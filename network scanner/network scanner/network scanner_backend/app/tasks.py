# app/tasks.py
from .celery_worker import celery
import subprocess
from flask_socketio import SocketIO
import os

nmap_path = os.getenv('NMAP_PATH', 'nmap')  # Default to 'nmap' if not set

@celery.task(bind=True)
def perform_nmap_scan(self, ip_address):
    cmd = [nmap_path, '-p-', '--top-ports', '10', ip_address]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            self.update_state(state='PROGRESS', meta={'output': output.strip()})
    process.poll()
