import os
import yt_dlp

def console_progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        
        if total > 0:
            percentage = (downloaded / total) * 100
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', 'N/A').strip()
            print(f"\rProgress: {percentage:.1f}% | Speed: {speed} | ETA: {eta}  ", end="", flush=True)
            
    elif d['status'] == 'finished':
        print("\nDownload finished! Processing media...")


def download_video(url, save_path=None, custom_filename=None, progress_callback=None):
    if not save_path:
        save_path = os.getcwd()

    if custom_filename:
        filename_template = f"{custom_filename}.%(ext)s"
    else:
        filename_template = "%(title)s.%(ext)s"

    file_name = os.path.join(save_path, filename_template)
    active_hook = progress_callback if progress_callback else console_progress_hook

    ydl_opts = {
        'format': 'bestvideo*+bestaudio/best',
        'outtmpl': file_name,
        'noplaylist': True,
        'windowsfilenames': True,
        'overwrites': False,
        'noprogress': True,
        'progress_hooks': [active_hook],
        'quiet': True,
        'noprogress': True,
        'color': 'never'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    link = input("Enter YouTube video URL: ").strip()

    folder_path = input("Enter full folder path to save video (or press Enter for current directory): ").strip()

    new_name = input("Enter custom filename (press Enter to keep original title): ").strip()

    download_video(link, folder_path, custom_filename=new_name if new_name else None)

    if link:
        download_video(link)
        print("\nFinished!")
    else:
        print("No URL provided.")