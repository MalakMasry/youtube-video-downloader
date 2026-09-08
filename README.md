# YouTube Video Downloader (GUI)

A Python GUI app made using CustomTkinter that uses yt-dlp to download YouTube videos from their links.

<img width="600" alt="App Demo" src="https://github.com/user-attachments/assets/bd360cae-7ace-498d-b5f9-60ad1069b72d" />

## Features
- **File Handling:** Allows the user to select their preferred file destination and rename the output file directly.
- **Progress Tracking:** Displays a live progress bar with download percentage, speed, and ETA metrics.
- **Error Handling:** Automatically catches invalid URLs, private/deleted videos, and write-permission issues.

## Tech Stack
- **Language:** Python 3.x
- **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Backend Core:** [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Concurrency:** `threading` (Python Standard Library)
- 
## Prerequisites (Windows)

Before running the application, ensure you have **FFmpeg** installed on your system. `yt-dlp` requires FFmpeg to process downloads and merge video/audio streams.

1. Open Command Prompt or PowerShell.
2. Run the following command:
   
   ```cmd
   winget install ffmpeg
   ```

## Prerequisites (Windows)

Before running the application, ensure you have **FFmpeg** installed on your system. `yt-dlp` requires FFmpeg to process downloads and merge video/audio streams.

1. Open Command Prompt or PowerShell.
2. Run the following command:
   
   ```cmd
   winget install ffmpeg
   ```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MalakMasry/youtube-video-downloader.git
   cd youtube-video-downloader
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```