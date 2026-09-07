import os
import threading
import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
from downloader import download_video

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YouTube Video Downloader")
app.geometry("520x530")

ctk.CTkLabel(app, text="YouTube Video Downloader", font=("Arial", 20)).pack(pady=15)

ctk.CTkLabel(app, text="Enter YouTube video URL:").pack(pady=2)
url_entry = ctk.CTkEntry(app, width=420)
url_entry.pack(pady=5)

ctk.CTkLabel(app, text="Save Location:").pack(pady=2)

folder_frame = ctk.CTkFrame(app, fg_color="transparent")
folder_frame.pack(pady=5)

folder_entry = ctk.CTkEntry(folder_frame, width=320, placeholder_text="Default: Current Directory")
folder_entry.pack(side="left", padx=(0, 10))

def browse_folder():
    selected_dir = filedialog.askdirectory(title="Select Download Folder")
    if selected_dir:
        folder_entry.delete(0, "end")
        folder_entry.insert(0, selected_dir)

browse_btn = ctk.CTkButton(folder_frame, text="Browse...", width=90, command=browse_folder)
browse_btn.pack(side="left")

ctk.CTkLabel(app, text="Enter custom filename (leave blank for default):").pack(pady=2)
filename_entry = ctk.CTkEntry(app, width=420)
filename_entry.pack(pady=5)

# --- Progress Bar & Status Widgets ---
progress_bar = ctk.CTkProgressBar(app, width=420)
progress_bar.pack(pady=(15, 5))
progress_bar.set(0)  # Reset to 0%

status_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
status_label.pack(pady=5)

# Progress Hook Callback
def gui_progress_hook(d):
    """Updates the CTkProgressBar and status_label in real-time."""
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)
        
        if total > 0:
            percent = downloaded / total  # Scale: 0.0 to 1.0 for CTkProgressBar
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', 'N/A').strip()

            progress_bar.set(percent)
            status_label.configure(
                text=f"Downloading: {int(percent * 100)}% | Speed: {speed} | ETA: {eta}",
                text_color="#5DADE2"
            )
            
    elif d['status'] == 'finished':
        progress_bar.set(1.0)
        status_label.configure(text="Download finished! Processing media...", text_color="#5DADE2")

def start_download():
    url = url_entry.get().strip()
    folder_path = folder_entry.get().strip() or None
    custom_filename = filename_entry.get().strip() or None

    if not url:
        status_label.configure(text="Error: Please enter a YouTube URL.", text_color="red")
        return

    if folder_path and not os.path.exists(folder_path):
        status_label.configure(text="Error: Selected save directory does not exist.", text_color="red")
        return

    # Reset UI State
    download_btn.configure(state="disabled")
    progress_bar.set(0)
    status_label.configure(text="Initializing download...", text_color="#5DADE2")

    def run_backend():
        try:
            # Pass our GUI hook function to download_video
            download_video(url, folder_path, custom_filename, progress_callback=gui_progress_hook)
            status_label.configure(text="Download Finished Successfully!", text_color="green")

        except yt_dlp.utils.DownloadError as e:
            err_msg = str(e)
            if "is not a valid URL" in err_msg:
                status_label.configure(text="Error: Invalid YouTube URL structure.", text_color="red")
            elif "Video unavailable" in err_msg:
                status_label.configure(text="Error: Video is private, deleted, or unavailable.", text_color="red")
            else:
                status_label.configure(text="Download failed. Check your link or internet connection.", text_color="red")

        except PermissionError:
            status_label.configure(text="Error: Permission denied when writing to chosen folder.", text_color="red")

        except Exception as e:
            status_label.configure(text=f"Error: {e}", text_color="red")
            
        finally:
            download_btn.configure(state="normal")  # Re-enable button when done

    download_thread = threading.Thread(target=run_backend, daemon=True)
    download_thread.start()

download_btn = ctk.CTkButton(app, text="Download Video", command=start_download, width=200)
download_btn.pack(pady=15)

app.mainloop()