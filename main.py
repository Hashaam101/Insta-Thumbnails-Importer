import instaloader
import os
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
import sys
import contextlib
import os
import cv2
import imageio
import requests
from tqdm import tqdm

# ---------- CONFIG ----------
OUTPUT_DIR = "Images/insta"       # Folder to save images
OUTPUT_FILE = "instagram_posts.ts" # Output file
URLS = []
with open("import-URLs.txt", "r") as f:
    URLS = [line.strip() for line in f.readlines()]
# ----------------------------


# Clear output directory with progress bar
import shutil
from tqdm import tqdm

# Delete old .ts file if exists
old_ts_file = "instagram_posts.ts"
if os.path.exists(old_ts_file):
    try:
        os.remove(old_ts_file)
        print(f"Deleted old {old_ts_file}\nDeleted old Media files")
    except Exception as e:
        print(f"Failed to delete {old_ts_file}: {e}")

if os.path.exists(OUTPUT_DIR):
    files = os.listdir(OUTPUT_DIR)
    for filename in tqdm(files, desc="Clearing insta dir", colour="red"):
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
else:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize instaloader
L = instaloader.Instaloader(download_pictures=False,
                            download_videos=False,
                            download_video_thumbnails=False,
                            download_comments=False,
                            save_metadata=False,
                            compress_json=False)

posts_data = []

for idx, url in enumerate(tqdm(URLS, desc="Processing URLs", colour="green"), start=1):
    shortcode = url.strip("/").split("/")[-1]
    image_path = ""
    title = ""
    description = ""
    with contextlib.redirect_stdout(open(os.devnull, 'w')):
        with contextlib.redirect_stderr(open(os.devnull, 'w')):
            try:
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                title = post.owner_username
                description = post.caption.replace("\n", " ") if post.caption else ""
                is_reel = "reel" in url
                if is_reel and post.video_url:
                    video_path = os.path.join(OUTPUT_DIR, f"{idx}.mp4")
                    gif_path = os.path.join(OUTPUT_DIR, f"{idx}.gif")
                    r = requests.get(post.video_url, stream=True)
                    total_size = int(r.headers.get('content-length', 0))
                    with open(video_path, "wb") as v, tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading Reel {idx}", colour="cyan") as pbar:
                        for chunk in r.iter_content(chunk_size=8192):
                            v.write(chunk)
                            pbar.update(len(chunk))
                    try:
                        vid = cv2.VideoCapture(video_path)
                        frames = []
                        fps = vid.get(cv2.CAP_PROP_FPS)
                        max_frames = int(fps * 5) if fps > 0 else 50  # 5 seconds or fallback 50 frames
                        frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
                        with tqdm(total=min(frame_count, max_frames), desc=f"Converting Reel {idx} to GIF", colour="magenta") as pbar:
                            success, frame = vid.read()
                            count = 0
                            while success and count < max_frames:
                                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frames.append(rgb_frame)
                                success, frame = vid.read()
                                count += 1
                                pbar.update(1)
                        vid.release()
                        imageio.mimsave(gif_path, frames, format='GIF', duration=0.05, loop=0)
                        os.remove(video_path)
                        image_path = f"/{OUTPUT_DIR}/{idx}.gif"
                    except Exception:
                        pass
                else:
                    L.download_pic(os.path.join(OUTPUT_DIR, f"{idx}"), post.url, mtime=None)
                    downloaded_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(f"{idx}") and f.endswith(".jpg")]
                    if downloaded_files:
                        temp_jpg_path = os.path.join(OUTPUT_DIR, downloaded_files[0])
                        image_path = f"/Images/insta/{idx}.jpg"
                    else:
                        image_path = ""
            except Exception:
                pass
    posts_data.append({
        "id": str(idx),
        "title": title,
        "image": image_path,
        "url": url,
        "description": description
    })



with tqdm(total=len(posts_data), desc="Creating ts file", colour="blue") as pbar:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for post in posts_data:
            f.write("\t{\n")
            f.write(f'\t\tid: "{post["id"]}",\n')
            f.write(f'\t\ttitle: "{post["title"]}",\n')
            # If image is empty and not a reel, set to .jpg
            if post["image"] and post["image"].endswith(".gif"):
                f.write(f'\t\timage: "{post["image"]}",\n')
            else:
                f.write(f'\t\timage: "/Images/insta/{post["id"]}.jpg",\n')
            f.write(f'\t\turl: "{post["url"]}",\n')
            f.write(f'\t\tdescription: "{post["description"]}",\n')
            f.write("\t},\n")
            pbar.update(1)
