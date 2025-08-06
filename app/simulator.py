import threading
import time
import random
from database import record_event, get_departments, start_campaign_db, stop_campaign_db
import subprocess

running = False
simulation_thread = None

def campaign_running():
    return running

def simulate_events():
    global running
    departments = get_departments()
    
    while running:
        time.sleep(random.randint(2, 8))  # Random interval between events
        
        if not running:
            break
            
        # Simulate random events for random departments
        department = random.choice(departments)
        action = random.choice(['clicked', 'ignored', 'reported'])
        
        # Simulate email and IP
        fake_email = f"user{random.randint(1, 100)}@company.com"
        fake_ip = f"192.168.1.{random.randint(1, 254)}"
        
        record_event(department, action, fake_email, fake_ip)
        print(f"Simulated: {department} - {action}")

def start_campaign():
    global running, simulation_thread
    if running:
        return False
    
    running = True
    start_campaign_db()
    
    # Run Ansible playbook
    try:
        result = subprocess.run(
            ["ansible-playbook", "-i", "inventory.ini", "app/ansible/playbook.yml"],
            capture_output=True,
            text=True
        )
        print("Ansible output:", result.stdout)
        if result.stderr:
            print("Ansible errors:", result.stderr)
    except Exception as e:
        print(f"Error running Ansible: {e}")
    
    # Start simulation thread
    simulation_thread = threading.Thread(target=simulate_events)
    simulation_thread.daemon = True
    simulation_thread.start()
    
    return True

def stop_campaign():
    global running
    if not running:
        return False
    
    running = False
    stop_campaign_db()
    
    # Wait for simulation thread to finish
    if simulation_thread and simulation_thread.is_alive():
        simulation_thread.join(timeout=2)
    
    return True