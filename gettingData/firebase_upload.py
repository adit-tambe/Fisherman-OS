import os
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import google.auth.credentials
from fish import fetch_incois_data_automated

class MockCredential(credentials.Base):
    def get_credential(self):
        return google.auth.credentials.AnonymousCredentials()

def upload_to_firebase():
    # Tell Firebase Admin SDK to use the local Firestore emulator
    os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
    
    # Provide the project ID that matches your .firebaserc
    os.environ["GCLOUD_PROJECT"] = "fishermanos"
    
    # Initialize the Firebase Admin SDK
    if not firebase_admin._apps:
        firebase_admin.initialize_app(MockCredential(), options={"projectId": "fishermanos"})
        
    db = firestore.client()
    
    print("Fetching INCOIS data...")
    # This will call the function we built earlier
    df = fetch_incois_data_automated()
    
    if isinstance(df, dict) and "error" in df:
        print("Error fetching data:", df)
        return
        
    print(f"Fetched {len(df)} records. Uploading to Firestore Emulator...")
    
    # Convert DataFrame to a list of dictionaries
    # Firestore doesn't support NaN values directly, so we need to handle them.
    # We replace NaN with None (which becomes null in JSON/Firestore)
    import math
    records = []
    for record in df.to_dict(orient="records"):
        clean_record = {}
        for k, v in record.items():
            if isinstance(v, float) and math.isnan(v):
                clean_record[k] = None
            else:
                clean_record[k] = v
        records.append(clean_record)
    
    batch = db.batch()
    collection_ref = db.collection("fishing_zones")
    
    count = 0
    for record in records:
        # Create a new document for each record
        doc_ref = collection_ref.document()
        batch.set(doc_ref, record)
        count += 1
        
        # Firestore batches support up to 500 operations
        if count % 500 == 0:
            batch.commit()
            batch = db.batch()
            
    # Commit any remaining operations in the batch
    if count % 500 != 0:
        batch.commit()
        
    print(f"Successfully uploaded {count} records to Firestore Emulator (collection: 'fishing_zones')!")

if __name__ == "__main__":
    upload_to_firebase()
