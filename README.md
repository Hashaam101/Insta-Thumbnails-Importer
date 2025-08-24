
# Insta-Thumbnails-Importer

### A recommended tool for instagram media downloading for TableTurnerr Child Site - Instagram section

Python script to download Instagram post thumbnails and reels, convert images to `.jpg` format for posts and `.gif` format for reels. All images are saved as `.jpg`, all reels as `.gif` (5 seconds, looped), and the output directory is cleared before each run. Progress bars are shown for downloads and conversions for a better terminal experience. Terminal is cleared at start and all error/info messages are suppressed except progress bars.

## Features
- Downloads Instagram post thumbnails as `.jpg` images
- Downloads Instagram reels as `.gif` files (first 5 seconds, looped, removes temporary `.mp4` after conversion)
- Clears output directory before each run
- Deletes old `.ts` file before each run
- Outputs a TypeScript file (`instagram_posts.ts`) with post metadata (IDs start from 1 and match URL order)
- Shows progress bars for downloads and conversions
- Easy configuration of URLs and output paths
- Clears terminal at start
- Suppresses all error/info messages except progress bars

## Requirements
- Python 3.7+
- See `requirements.txt` for dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Edit the `URLS` list in `main.py` to add your Instagram post/reel URLs.
2. Run the script:
```bash
python main.py
```
3. Find the converted images/gifs in the `Images/insta/` folder and metadata in `instagram_posts.ts`.

## Output
- Images: `Images/insta/*.jpg`
- Reels: `Images/insta/*.gif` (first 5 seconds, looped, no `.mp4` files kept)
- Metadata: `instagram_posts.ts` (IDs start from 1 and match URL order)

## Notes
- Instagram posts are saved as `.jpg` images.
- Instagram reels are saved as `.gif` files (first 5 seconds, looped, temporary `.mp4` files are deleted after conversion).
- The script does not require login for public posts/reels.
- Progress bars are shown for downloads and conversions.
- Terminal is cleared at start and all error/info messages are suppressed except progress bars.

## Rights
TableTurnerr.com -- Code generated with AI Assistance
