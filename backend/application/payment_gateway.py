import requests
import json
import asyncio
from vsystech_users_models import PaymentGateway
import sys
import os
sys.path.append(os.getcwd() + "framework/")
from queryparams import QueryParams


def getgatewayName(paymentgateway):
    gateways = {
        "PayPal": PayPal,
    }
    return gateways[paymentgateway]


class PaymentGateways:
    
    async def verifyCredential(self, gatwayName):
        pass
    
    async def createOrder(self,data):
        pass

    async def verifyOrder(self, data):
        pass

class PayPal(PaymentGateways):
    
    async def verifyCredential(self,gatwayName):
        await super().verifyCredential(gatwayName)
        query = {"gateway.gateway_name": gatwayName, "is_verified": True}
        data =  await PaymentGateway.get_all(QueryParams(q=json.dumps(query), limit=1))
        if not data.get("data", []):
            return {"status": False, "msg": "No creds found"}
        data = data["data"][0]
        base_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        reqdata = {
            "grant_type": "client_credentials"
        }

        sendRequest = requests.post(base_url, 
                        headers=headers, 
                        data=reqdata, 
                        auth=requests.auth.HTTPBasicAuth(data["gateway"]["api_key"], data["gateway"]["api_secret"])
        )
        if not sendRequest.status_code == 200:
            return {"status": False, "msg": "Invalid creds"}
        return  {"status": True, "data": sendRequest.json(), "gateway_details": data}
    async def createOrder(self, data):
        await super().createOrder(data)
        creds = await self.verifyCredential(data["gateway_name"])
        if not creds.get("status", False):
            return {"status": False, "msg": "No creds found"}
        gateway_details = creds["gateway_details"]
        creds = creds["data"]
        headers = {
            'Content-Type': 'application/json',
            'PayPal-Request-Id': data["id"],
            # 'Authorization': f'Basic {creds["gateway"]["api_key"]}:{creds["gateway"]["api_secret"]}',
            'Authorization': f'Bearer {creds["access_token"]}',
        }
        inpData = json.dumps({ 
            "intent": "CAPTURE", 
            "purchase_units": [ 
                { 
                    "reference_id": data["id"], 
                    "amount": { "currency_code": "USD", "value": data["order_amt"] } ,
                    "shipping": {
                        "address": {
                            "address_line_1": "1211 North Underhill Street",
                            "admin_area_2": "Peoria",
                            "admin_area_1": "IL",
                            "postal_code": "61604",
                            "country_code": "US"
                        }
                    }
                }
            ],
            "payment_source": { 
                "paypal": { 
                    "experience_context": { 
                        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", 
                        "brand_name": "VSYSTECH", 
                        "locale": "en-US", 
                        "landing_page": "LOGIN", 
                        "shipping_preference": "SET_PROVIDED_ADDRESS", 
                        "user_action": "PAY_NOW", 
                        "return_url": "https://app.vsystech.net/verifyPayment", 
                        "cancel_url": "https://example.com/cancelUrl" 
                    } 
                } 
            }
        })
        # inpData = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b", "amount": { "currency_code": "USD", "value": "100.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "shipping_preference": "SET_PROVIDED_ADDRESS", "user_action": "PAY_NOW", "return_url": "https://example.com/returnUrl", "cancel_url": "https://example.com/cancelUrl" } } } }'

        createPayment = requests.post(
            gateway_details["gateway"]["base_url"] + "/checkout/orders", 
            headers=headers,
            data=inpData
        )
        if createPayment.status_code != 200:
            return {"status": False, "msg": "Payment not created"}
        payment_data = createPayment.json()
        payment_data["payment_url"] = gateway_details["gateway"]["base_url"] + f"/checkout/orders/{payment_data['id']}/capture"
        return {"status": True, "data": payment_data}



    async def verifyOrder(data):
        await super().verifyOrder(data)
        pass

