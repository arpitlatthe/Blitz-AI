import os
import streamlit as st

import firebase_admin
from firebase_admin import credentials, firestore


if not firebase_admin._apps:

    if "firebase" in st.secrets:

        firebase_credentials = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace(
                "\\n", "\n"
            ),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"][
                "auth_provider_x509_cert_url"
            ],
            "client_x509_cert_url": st.secrets["firebase"][
                "client_x509_cert_url"
            ]
        }

        cred = credentials.Certificate(firebase_credentials)

    else:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        KEY_PATH = os.path.join(
            BASE_DIR,
            "serviceAccountKey.json"
        )

        cred = credentials.Certificate(KEY_PATH)

    firebase_admin.initialize_app(cred)


db = firestore.client()