import threading, time
from database import record_event
import subprocess

running = False

def campaign_running():
    return running

def simulate_events():
    global running
    while running:
        time.sleep(3)
        record_event("clicked")
        record_event("ignored")
        record_event("reported")

def start_campaign():
    global running
    if running: return
    running = True
    subprocess.run(["ansible-playbook", "-i", "inventory.ini", "app/ansible/playbook.yml"])
    threading.Thread(target=simulate_events).start()

def stop_campaign():
    global running
    running = False