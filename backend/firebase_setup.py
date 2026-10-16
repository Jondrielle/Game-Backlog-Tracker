import os
import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    if not firebase_admin._apps:
        key_path = os.environ["FIREBASE_SERVICE_ACCOUNT_PATH"]
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)