from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Solo reinicia el servicio si el evento es sobre un archivo (no un directorio)
        if not event.is_directory:
            print(f'Event type: {event.event_type}  Path: {event.src_path}')
            # Reinicia el servicio
            try:
                subprocess.run(['sudo', 'systemctl', 'restart', 'chatbot.service'], check=True)
                print('chatbot.service has been restarted.')
                print(f'STDOUT: {result.stdout.decode()}')
                print(f'STDERR: {result.stderr.decode()}')
            except subprocess.CalledProcessError as e:
                print(f'Error restarting chatbot.service: {e}')

path = "/var/www/chatbot_app"
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
