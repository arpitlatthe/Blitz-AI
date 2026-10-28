import os
import streamlit as st

import firebase_admin
from firebase_admin import credentials, firestore


if not firebase_admin._apps:

    try:
        firebase_secrets = st.secrets["firebase"]

        firebase_credentials = {
            "type": firebase_secrets["type"],
            "project_id": firebase_secrets["project_id"],
            "private_key_id": firebase_secrets["private_key_id"],
            "private_key": firebase_secrets["private_key"].replace(
                "\\n", "\n"
            ),
            "client_email": firebase_secrets["client_email"],
            "client_id": firebase_secrets["client_id"],
            "auth_uri": firebase_secrets["auth_uri"],
            "token_uri": firebase_secrets["token_uri"],
            "auth_provider_x509_cert_url": firebase_secrets[
                "auth_provider_x509_cert_url"
            ],
            "client_x509_cert_url": firebase_secrets[
                "client_x509_cert_url"
            ]
        }

        cred = credentials.Certificate(firebase_credentials)

    except Exception:

        # Local development
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        KEY_PATH = os.path.join(
            BASE_DIR,
            "serviceAccountKey.json"
        )

        cred = credentials.Certificate(KEY_PATH)

    firebase_admin.initialize_app(cred)


db = firestore.client()