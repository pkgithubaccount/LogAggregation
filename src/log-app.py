import os
import logging
import tkinter as tk
from tkinter import filedialog, scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import shutil

# Constants
LOG_FILE = 'aggregated.log'
LOG_DIR = 'log_files'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB

# Setup logging
def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LogHandler(FileSystemEventHandler):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def on_modified(self, event):
        if not event.is_directory:
            with open(event.src_path, 'r') as file:
                content = file.read()
                self.text_widget.insert(tk.END, content)
                self.text_widget.yview(tk.END)  # Scroll to the end

def rotate_logs():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        rotated_log = f'{LOG_FILE}_{timestamp}'
        shutil.move(LOG_FILE, rotated_log)
        logging.info(f'Log rotated to {rotated_log}')

def start_monitoring(folder_path, text_widget):
    event_handler = LogHandler(text_widget)
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=True)
    observer.start()

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        start_monitoring(folder_path, log_display)
        log_display.insert(tk.END, f'Monitoring folder: {folder_path}\n')
        log_display.yview(tk.END)

def clear_log():
    log_display.delete('1.0', tk.END)

# Create the main window
root = tk.Tk()
root.title('Log Aggregation Tool')

# Create the GUI elements
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

browse_button = tk.Button(frame, text='Browse Folder', command=browse_folder)
browse_button.pack(side=tk.LEFT)

clear_button = tk.Button(frame, text='Clear Log', command=clear_log)
clear_button.pack(side=tk.LEFT)

log_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
log_display.pack(padx=10, pady=10)

# Setup logging
setup_logging()

# Rotate logs every 10 minutes
root.after(600000, rotate_logs)

# Start the GUI event loop
root.mainloop()
