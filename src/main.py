"""
YouTube Video Downloader Module
===============================

This script provides a clean, object-oriented interface for downloading 
YouTube videos using the `pytubefix` library.
"""

from pathlib import Path
from typing import Optional, Union, Any

from pytubefix import YouTube
from pytubefix.cli import on_progress


class YouTubeDownloader:
    """
    A utility class to manage and execute YouTube video downloads.
    """

    def __init__(self, url: str, output_path: Optional[Union[str, Path]] = None, quality: Optional[str] = None) -> None:
        """
        Initialize the YouTubeDownloader.

        :param url: The URL of the YouTube video to download.
        :param output_path: The directory where the video will be saved. Defaults to './downloaded_files'.
        :param quality: The desired resolution (e.g., '720p', '1080p', or 'lowest'). Defaults to highest available.
        """
        self.url: str = url
        self.output_path: Path = Path(output_path) if output_path else Path.cwd() / "downloaded_files"
        self.quality: Optional[str] = quality
        
        # Ensure the output directory exists before downloading
        self.output_path.mkdir(parents=True, exist_ok=True)

        self.yt: YouTube = YouTube(
            self.url,
            on_progress_callback=on_progress,
            on_complete_callback=self.on_complete
        )

    def download(self) -> None:
        """
        Execute the download process based on the specified quality.
        
        :raises ValueError: If the specified quality stream cannot be found.
        """
        if self.quality == "lowest":
            stream = self.yt.streams.get_lowest_resolution()
        elif self.quality:
            stream = self.yt.streams.filter(
                progressive=True,
                file_extension='mp4',
                res=self.quality
            ).first()
        else:
            # Default to the highest resolution available if no quality is specified
            stream = self.yt.streams.get_highest_resolution()

        if not stream:
            raise ValueError(f"Could not find an mp4 video stream matching quality: {self.quality}")

        print(f"Starting download: '{self.yt.title}'...")
        # pytubefix generally expects a string for the output_path argument
        stream.download(output_path=str(self.output_path))

    def on_complete(self, stream: Any, file_path: str) -> None:
        """
        Callback triggered when the download finishes successfully.

        :param stream: The stream that was downloaded.
        :param file_path: The absolute path to the saved file.
        """
        print(f"\nSuccess! Download complete. File saved to: {file_path}")


if __name__ == "__main__":
    target_url = "https://youtu.be/m4wllxpGKew?si=dCcA1cwUyn_9udAU"
    
    try:
        # Example usage: downloading at 720p (if available)
        video_downloader = YouTubeDownloader(target_url, quality="720p")
        video_downloader.download()
    except Exception as e:
        print(f"An error occurred during execution: {e}")
