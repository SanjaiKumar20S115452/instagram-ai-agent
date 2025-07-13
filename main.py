import requests
import os
from dotenv import load_dotenv
from json_loader import load_memes, get_unposted_memes
from firebase_utils import initialize_firebase, load_posted, save_posted
import random

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")

def create_instagram_post(image_url, caption):
    # Step 1: Create media container
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}/media"
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url=url, data=params)
    result = res.json()
    creation_id = result.get("id")

    if not creation_id:
        print("❌ Error creating media container:", result)
        return False
    
    # Step 2: Publish the media
    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}/media_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    publish_res = requests.post(publish_url, data=publish_params)
    print("✅ Post published:", publish_res.json())
    return True

def main():
    initialize_firebase()
    posted_set = load_posted()
    all_memes = load_memes("memes.json")
    unposted_memes = get_unposted_memes(all_memes, posted_set)

    if not unposted_memes:
        print("🎉 All memes have been posted!")
        return

    meme = random.choice(unposted_memes)
    caption = f"📘 {meme['word']}\n\n🧠 Definition: {meme['definition']}\n#Wordcorn #GREvocab"
    
    if create_instagram_post(meme['memeurl'], caption):
        posted_set.add(meme['word'])
        save_posted(posted_set)
        print(f"✅ Successfully posted '{meme['word']}' to Instagram.")
    else:
        print(f"❌ Failed to post '{meme['word']}'.")

if __name__ == "__main__":
    main()
