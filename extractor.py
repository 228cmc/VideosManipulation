import os
import re
import subprocess
import cv2
from youtube_transcript_api import YouTubeTranscriptApi
from tqdm import tqdm

class YouTubeProcessor:
    def __init__(self, video_url, language="en", output_folder="screenshots", screenshot_interval=5):
        self.video_url = video_url
        self.language = language
        self.output_folder = output_folder
        self.screenshot_interval = screenshot_interval
        self.video_id = self._extract_video_id()
        self.video_path = None  

        os.makedirs(self.output_folder, exist_ok=True)

    def _extract_video_id(self):
        """Extracts the video ID from a YouTube URL."""
        match = re.search(r"v=([a-zA-Z0-9_-]+)", self.video_url)
        return match.group(1) if match else None

    def extract_subtitles(self):
        """Extracts and saves subtitles in an .srt file."""
        if not self.video_id:
            print("Error: Could not extract the video ID.")
            return None

        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages=[self.language])
            file_path = os.path.join(self.output_folder, f"subtitles_{self.video_id}.srt")

            if not transcript:
                print("Warning: No subtitles found for this video.")
                return None

            print(f"Writing subtitles to {file_path}...")

            with open(file_path, "w", encoding="utf-8") as file:
                for i, line in enumerate(transcript, start=1):
                    start_time = line['start']
                    end_time = start_time + line['duration']
                    text = line['text']
                    file.write(f"{i}\n{start_time:.3f} --> {end_time:.3f}\n{text}\n\n")

            print(f"Subtitles saved: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error extracting subtitles: {e}")
            return None

    def download_video(self):
        """Downloads the YouTube video using yt-dlp."""
        if not self.video_id:
            print("Error: Could not extract the video ID.")
            return None

        self.video_path = os.path.join(self.output_folder, f"{self.video_id}.mp4")

        try:
            print(f"Downloading video: {self.video_url}")
            subprocess.run(
                ["yt-dlp", "-f", "best", "-o", self.video_path, self.video_url],
                check=True,
            )
            print(f"Video downloaded: {self.video_path}")
            return self.video_path
        except subprocess.CalledProcessError as e:
            print(f"Error downloading video: {e}")
            return None

    def extract_screenshots(self):
        """Extracts screenshots from video at the given interval."""
        if not self.video_path or not os.path.exists(self.video_path):
            print("Error: Video file not found.")
            return

        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.screenshot_interval)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"Extracting screenshots every {self.screenshot_interval} seconds...")

        for frame_number in tqdm(range(0, total_frames, frame_interval)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = cap.read()
            if success:
                timestamp = int(frame_number / fps)
                screenshot_path = os.path.join(self.output_folder, f"screenshot_{timestamp}s.jpg")
                cv2.imwrite(screenshot_path, frame)
                print(f"Saved screenshot: {screenshot_path}")
            else:
                print(f"Error capturing screenshot at {timestamp}s")

        cap.release()
