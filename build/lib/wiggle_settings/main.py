import json
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import stat
from threading import Timer
from pathlib import Path

current_file_path = Path(__file__).resolve()
current_dir = current_file_path.parent
neopixels_path = current_dir / 'neopixels' / 'neopixels.py'

SETTINGS_FILE = "/etc/settings.json"
DEFAULT_SETTINGS_FILE = str(current_dir / 'default.json')

class Status:
    ON = "on"
    OFF = "off"

def read_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            delay = 0.2
            time.sleep(delay)
            settings = json.load(file)
    else:
        with open(DEFAULT_SETTINGS_FILE, 'r') as default_file:
            settings = json.load(default_file)
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file, indent=4)

        # Change file permissions to allow group write
        os.chmod(SETTINGS_FILE, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)        # Change group ownership to 'mygroup'
    return settings

def update_settings(new_settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(new_settings, file, indent=4)

def update_setting(key, status):
    settings = read_settings()
    settings[key] = status
    update_settings(settings)

class SettingsChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.timer = None

    def on_modified(self, event):
        if event.src_path == str(SETTINGS_FILE):
            # Prevents multiple calls to callback when saving a file
            if self.timer is not None:
                self.timer.cancel()
            self.timer = Timer(0.1, self.callback)
            self.timer.start()

def monitor_settings_file(callback):
    event_handler = SettingsChangeHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(SETTINGS_FILE), recursive=False)
    observer.start()
    return observer

def trigger_settings_change():
    settings = read_settings()

    if settings["light"] == Status.ON:
        subprocess.run(['sudo', 'wiggle-light', '--on', '0.1'])
    elif settings["light"] == Status.OFF:
        subprocess.run(['sudo', 'wiggle-light', '--off'])

    if settings["recording"] == Status.ON:
        subprocess.run(['wiggle-camera', '--service', 'start'])
    elif settings["recording"] == Status.OFF:
        subprocess.run(['wiggle-camera', '--service', 'stop'])

def main():
    trigger_settings_change()
    observer = monitor_settings_file(trigger_settings_change)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()