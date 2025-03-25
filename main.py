import os
import sys
from dotenv import load_dotenv
from extractor import YouTubeProcessor

# Load environment variables
load_dotenv()

def main():
    video_url = os.getenv("YOUTUBE_VIDEO_URL")
    language = os.getenv("SUBTITLE_LANGUAGE", "en")
    output_folder = os.getenv("OUTPUT_FOLDER", "screenshots")
    screenshot_interval = int(os.getenv("SCREENSHOT_INTERVAL", 5))

    if not video_url:
        print("Error: No video URL found in .env file. Please set YOUTUBE_VIDEO_URL.")
        sys.exit(1)

    processor = YouTubeProcessor(video_url, language, output_folder, screenshot_interval)

    processor.extract_subtitles()  
    video_path = processor.download_video()  

    if video_path:
        processor.extract_screenshots()  

if __name__ == "__main__":
    main()
