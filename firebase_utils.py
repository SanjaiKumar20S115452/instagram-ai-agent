import os 
import json
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    if not firebase_admin._apps:
        firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
        if not firebase_creds:
            raise Exception("FIREBASE CREDENTIALS not set.")
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://instagram-ai-agent-bcb40-default-rtdb.firebaseio.com/'
    })

def get_posts():
    ref = db.reference("posts")
    return ref.get() or {}

def load_posted_from_firebase():
    try:
        ref = db.reference("posted_memes")
        data = ref.get()
        return set(data or [])
    except Exception as e:
        print("Error loading from Firebase:", str(e))
        return set()
    
def save_posted_to_firebase(posted_set):
    try: 
        ref = db.reference("posted_memes")
        ref.set(list(posted_set))
    except Exception as e:
        print("Error saving to Firebase:", str(e))