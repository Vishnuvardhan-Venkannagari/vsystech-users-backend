#
BACKEND/
│
├── adminportal/                # Admin-specific logic
│
├── application/                # Core application logic
│   ├── users_createUserWithEmail.py
│   ├── users_updateUser.py
│   ├── users_uploadPicture.py
│   ├── utilities.py
│   ├── vsystech_users_enum.py
│   ├── vsystech_users_models.py
│   ├── vsystech_users_roles.json
│   └── vsystech_users_stdapi.py
│
├── framework/                  # Framework-related logic 
│   ├── __main__.py             # pip install -e .
│   ├── context.py              # pip install .
│   ├── firebasemodel.py
│   ├── queryparms.py
│   ├── redispool.py
│   └── restapi.py
│
├── .gitignore                  # Files to be ignored by Git
├── appspec.yml                 # AWS CodeDeploy configuration (if applicable)
├── codeupdate.sh               # Script for code deployment
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
