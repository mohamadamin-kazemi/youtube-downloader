# YouTube Video Downloader

A clean, object-oriented command-line interface (CLI) utility for downloading YouTube videos. Built with Python, this tool utilizes the `pytubefix` library for robust downloading capabilities and `tqdm` to provide a real-time visual progress bar. 

## ✨ Features

* **Simple CLI:** Easy-to-use command-line interface with intuitive arguments.
* **Quality Selection:** Downloads the highest available resolution by default, or allows you to specify a desired quality (e.g., '720p', '1080p', or 'lowest').
* **Custom Output Paths:** Choose exactly where your downloaded videos are saved. Automatically creates the directory if it doesn't exist.
* **Progress Tracking:** Interactive download progress bar via `tqdm`.
* **Error Handling:** Gracefully handles unavailable videos and keyboard interrupts.

## 📂 Project Structure

```text
youtube-downloader/
├── src/
│   └── main.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## 🚀 Installation

### 1. Clone the repository
```bash
git clone [https://github.com/mohamadamin-kazemi/youtube-downloader.git](https://github.com/mohamadamin-kazemi/youtube-downloader.git)
cd youtube-downloader
```

### 2. Install dependencies
It is recommended to use a virtual environment. Install the packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(Dependencies include `pytubefix==10.7.3` and `tqdm==4.67.3`)*

## 💻 Usage

Run the script from your terminal using Python. The only required argument is the YouTube video URL.

### Basic Usage
To download a video at the highest available resolution to the default `./downloaded_files` directory:
```bash
python src/main.py "[https://www.youtube.com/watch?v=YOUR_VIDEO_ID](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)"
```

### Advanced Usage
To specify a download quality and a custom output directory:
```bash
python src/main.py "[https://www.youtube.com/watch?v=YOUR_VIDEO_ID](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)" -q 720p -o /path/to/save/directory
```

### Command-Line Arguments

| Argument | Short | Description | Default |
| :--- | :--- | :--- | :--- |
| `url` | | **(Required)** The full URL of the YouTube video. | None |
| `--quality` | `-q` | The desired video quality (e.g., `720p`, `1080p`, `lowest`). | Highest resolution |
| `--output` | `-o` | The destination directory path for the downloaded file. | `./downloaded_files` |

## 📄 License

This project includes a `LICENSE` file. Please refer to the repository for more details regarding distribution and modification rights.