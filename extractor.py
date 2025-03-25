import os
import re
import sys
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env file
load_dotenv()

# Extract video ID from the YouTube URL
def get_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

# Fetch and save subtitles in an .srt file
def extract_subtitles(video_url, language="en"):
    video_id = get_video_id(video_url)
    if not video_id:
        print("Error: Could not extract the video ID.")
        return

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        with open(f"subtitles_{video_id}.srt", "w", encoding="utf-8") as file:
            for i, line in enumerate(transcript, start=1):
                start_time = line['start']
                end_time = start_time + line['duration']
                text = line['text']
                file.write(f"{i}\n{start_time:.3f} --> {end_time:.3f}\n{text}\n\n")

        print(f"Subtitles saved as: subtitles_{video_id}.srt")

    except Exception as e:
        print(f"Error: {e}")

# Main execution
if __name__ == "__main__":
    video_url = os.getenv("YOUTUBE_VIDEO_URL")
    language = os.getenv("SUBTITLE_LANGUAGE", "en")  # Default to English

    if not video_url:
        print("Error: No video URL found in .env file. Please set YOUTUBE_VIDEO_URL.")
        sys.exit(1)

    extract_subtitles(video_url, language)
