"""
YouTube Video Downloader Module
===============================

This script provides a clean, object-oriented interface for downloading 
YouTube videos using the `pytubefix` library, featuring a CLI and progress bar.
"""

import argparse
from pathlib import Path
from typing import Optional, Union, Any

from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
from tqdm import tqdm


class YouTubeDownloader:
    """
    A utility class to manage and execute YouTube video downloads.
    """

    def __init__(self, url: str, output_path: Optional[Union[str, Path]] = None, quality: Optional[str] = None) -> None:
        """
        Initialize the YouTubeDownloader.

        :param url: The URL of the YouTube video to download.
        :type url: str
        :param output_path: The directory where the video will be saved. Defaults to './downloaded_files'.
        :type output_path: Optional[Union[str, Path]]
        :param quality: The desired resolution (e.g., '720p', '1080p', or 'lowest'). Defaults to highest available.
        :type quality: Optional[str]
        """
        self.url: str = url
        self.output_path: Path = Path(output_path) if output_path else Path.cwd() / "downloaded_files"
        self.quality: Optional[str] = quality
        self.pbar: Optional[tqdm] = None
        
        # Ensure the output directory exists before downloading
        self.output_path.mkdir(parents=True, exist_ok=True)

        self.yt: YouTube = YouTube(
            self.url,
            on_progress_callback=self.on_progress,
            on_complete_callback=self.on_complete
        )

    def download(self) -> None:
        """
        Execute the download process based on the specified quality.
        
        :raises ValueError: If the specified quality stream cannot be found.
        """
        try:
            self.yt.check_availability()
        except VideoUnavailable:
            print(f"Error: The video at URL '{self.url}' is unavailable or restricted.")
            return
        
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

        self.pbar = tqdm(
            desc=f"Downloading: '{self.yt.title}'",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            total=stream.filesize
        )

        # pytubefix generally expects a string for the output_path argument
        stream.download(output_path=str(self.output_path))

    def on_progress(self, stream: Any, chunk: bytes, bytes_remaining: int) -> None:
        """
        Callback triggered as the video downloads to update the progress bar.

        :param stream: The stream being downloaded.
        :type stream: Any
        :param chunk: The segment of data just downloaded.
        :type chunk: bytes
        :param bytes_remaining: The number of bytes left to download.
        :type bytes_remaining: int
        """
        if self.pbar:
            current = stream.filesize - bytes_remaining
            self.pbar.update(current - self.pbar.n)

    def on_complete(self, stream: Any, file_path: str) -> None:
        """
        Callback triggered when the download finishes successfully.

        :param stream: The stream that was downloaded.
        :type stream: Any
        :param file_path: The absolute path to the saved file.
        :type file_path: str
        """
        if self.pbar:
            self.pbar.close()
        print(f"\nSuccess! Download complete. File saved to: {file_path}")


def main() -> None:
    """
    Main controller for parsing CLI arguments and executing the downloader.
    """
    parser = argparse.ArgumentParser(description='YouTube Video Downloader')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-q', '--quality', help='Video quality (e.g., 720p, 1080p, lowest)', default=None)
    parser.add_argument('-o', '--output', help='Output directory path', default=None)
    args = parser.parse_args()
    
    try:
        video_downloader = YouTubeDownloader(
            url=args.url,
            output_path=args.output,
            quality=args.quality
        )
        video_downloader.download()
    except KeyboardInterrupt:
        print("\nDownload cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")


if __name__ == "__main__":
    main()
