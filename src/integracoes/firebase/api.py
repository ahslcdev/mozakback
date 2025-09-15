import json
import os

import firebase_admin
from firebase_admin import credentials

from core.settings import env


def initialize_firebase():
    if firebase_admin._apps:
        return firebase_admin.get_app()
    json_path = env("FIREBASE_JSON_PATH")
    raw_json = ""
    if json_path and os.path.exists(json_path):
        cred = credentials.Certificate(json_path)
    elif raw_json:
        cred_dict = json.loads(raw_json)
        cred = credentials.Certificate(cred_dict)
    else:
        raise RuntimeError("Configure a variável de ambiente FIREBASE_JSON_PATH.")

    return firebase_admin.initialize_app(cred)


_default_app = initialize_firebase()
