import schedule
import time
from firebase_utils import initialize_firebase, get_posts, load_posted_from_firebase, save_posted_to_firebase
from main import create_instagram_post

def job():
    print("Running scheduled job...")
    initialize_firebase()
    posted_set = load_posted_from_firebase
    posts = get_posts()

    for _, post in posts.items():
        image_url = post.get("image_url")
        title = post.get("title", "")
        description = post.get("description", "")
        caption = f"{title}\n\n{description}"

        if image_url in posted_set:
            print(f"Already posted: {image_url}")
            continue

        print(f"Posting to Instagram: {title}")
        create_instagram_post(image_url=image_url, caption=caption)
        posted_set.add(image_url)
        save_posted_to_firebase(posted_set=posted_set)
        break

schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    print("Instagram Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)