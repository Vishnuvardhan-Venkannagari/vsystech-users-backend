# import openai
# from typing import Optional
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY")

# system_prompt = """Updated policies as of 2024-01:
# - New holiday return window: 45 days
# - Crypto refunds now supported"""


# # async def detect_intent(message: str) -> str:
# #     keywords = {
# #         "return": ["return", "send back"],
# #         "refund": ["refund", "money back"],
# #         "tracking": ["track", "where is"]
# #     }
# #     message = message.lower()
# #     for intent, terms in keywords.items():
# #         if any(term in message for term in terms):
# #             return intent
# #     return "general"


# # async def get_ai_response(self, message: str, chat_history: list) -> Optional[dict]:
# #     try:
# #         intent = await detect_intent(message)
# #         if intent in SIMPLE_INTENTS:  
# #             return {
# #                 "message": PREDEFINED_RESPONSES[intent],
# #                 "confidence": 1.0,
# #                 "needs_escalation": False
# #             }
# #         response = await openai.ChatCompletion.acreate(
# #             model="gpt-3.5-turbo",
# #             messages=[
# #                 {"role": "system", "content": "You're a customer support assistant. Be concise."},
# #                 *chat_history,
# #                 {"role": "user", "content": message}
# #             ],
# #             temperature=0.7
# #         )
# #         ai_message = response.choices[0].message.content
# #         needs_escalation = ("connect you" in ai_message.lower() or 
# #                        len(ai_message) < 15)
# #         return {
# #             "message": ai_message,
# #             "confidence": 1.0,
# #             "needs_escalation": needs_escalation
# #         }
# #     except Exception as e:
# #         print(f"OpenAI error: {e}")
# #         return None

# async def get_ai_response(message: str) -> dict:
#     """Pure AI endpoint with embedded knowledge"""
#     response = await openai.ChatCompletion.acreate(
#         max_tokens=150,
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You're a support agent for VSYSTECH (e-commerce). Key policies:
# - Returns: 30-day window, contact returns@vsystech.com
# - Refunds: 5-7 business days
# - Tracking: Use app.vsystech.net/track

# Rules:
# 1. NEVER make up policies
# 2. For unknowns: "I'll connect you to a specialist\"""" 
#             },
#             {"role": "user", "content": message}
#         ],
#         temperature=0.3  # Balance creativity/accuracy
#     )
    
#     ai_message = response.choices[0].message.content
#     return {
#         "message": ai_message,
#         "needs_escalation": "connect you" in ai_message.lower()
#     }

# def should_escalate(ai_message: str) -> bool:
#     triggers = [
#         "connect you", 
#         "specialist",
#         "I can't determine",
#         len(ai_message.split()) < 10  # Very short responses
#     ]
#     return any(trigger in ai_message.lower() for trigger in triggers)



import openai
import asyncio
from typing import Optional, List, Dict
import os
# from functools import lru_cache

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You're a support agent for VSYSTECH. Key policies:
- Returns: 30-day window
- Refunds: 5-7 business days
Rules:
1. Be concise
2. Escalate if unsure"""

def should_escalate(response: str) -> bool:
    triggers = [
        "connect you",
        "specialist",
        "I can't",
        len(response.split()) < 10
    ]
    return any(trigger.lower() in response.lower() for trigger in triggers)

async def get_ai_response(message: str, history: List[Dict] = None) -> Dict:
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        if history:
            messages.extend(history[-3:]) 
            
        messages.append({"role": "user", "content": message[:500]}) 
        
        # response = await openai.ChatCompletion.acreate(
        #     model="gpt-3.5-turbo",
        #     messages=messages,
        #     temperature=0.3,
        #     max_tokens=150,
        #     timeout=10  
        # )
        response = await asyncio.wait_for(
            openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3,
                max_tokens=150
            ),
            timeout=10
        )
        ai_message = response.choices[0].message.content
        return {
            "message": ai_message,
            "needs_escalation": should_escalate(ai_message)
        }
        
    except asyncio.TimeoutError:
        return {"message": "Response took too long. Connecting you to support.", "needs_escalation": True}
    except openai.error.RateLimitError:
        return {"message": "Our systems are busy. Please try again later.", "needs_escalation": True}
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return {"message": "Technical issue - connecting you to support", "needs_escalation": True}