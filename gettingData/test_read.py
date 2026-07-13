import os
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import google.auth.credentials

class MockCredential(credentials.Base):
    def get_credential(self):
        return google.auth.credentials.AnonymousCredentials()

# Tell Firebase Admin SDK to use the local Firestore emulator
os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
os.environ["GCLOUD_PROJECT"] = "demo-project"

firebase_admin.initialize_app(MockCredential(), options={"projectId": "demo-project"})
db = firestore.client()

docs = list(db.collection("fishing_zones").stream())
print(f"Found {len(docs)} documents in 'demo-project' fishing_zones collection!")
