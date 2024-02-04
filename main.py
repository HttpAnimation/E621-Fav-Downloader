import os
import time
import requests
from config import username, api_key

# API endpoint URLs
favorites_url = f"https://e621.net/favorites.json?user_id={username}"
download_base_url = "https://e621.net/posts/"

# Directory to save downloaded images
download_directory = "e621_favorites"

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

# Set up headers with user-agent and authorization
headers = {
    "User-Agent": "MyProject/1.0 (by your_username on e621)",
    "Authorization": f"Basic {username}:{api_key}"
}

def download_post(post_id, file_url):
    response = requests.get(file_url, headers=headers, stream=True)
    if response.status_code == 200:
        # Extract file extension from URL
        file_extension = file_url.split(".")[-1]
        # Save the image to the download directory
        file_path = os.path.join(download_directory, f"{post_id}.{file_extension}")
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download post {post_id}")

def get_user_favorites():
    response = requests.get(favorites_url, headers=headers)
    if response.status_code == 200:
        favorites = response.json()
        return favorites["posts"]
    else:
        print("Failed to retrieve favorites.")
        return []

def main():
    while True:
        try:
            # Get the user's favorites
            favorites = get_user_favorites()

            # Download new favorites
            for post in favorites:
                post_id = post["id"]
                file_url = post["file"]["url"]
                download_post(post_id, file_url)

            # Wait for 20 seconds before checking again
            time.sleep(20)
        except KeyboardInterrupt:
            print("Script terminated by user.")
            break

if __name__ == "__main__":
    main()
