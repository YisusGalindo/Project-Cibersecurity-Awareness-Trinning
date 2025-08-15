import threading
import time
import random
from database import record_event, get_departments, start_campaign_db, stop_campaign_db
import subprocess

running = False
simulation_thread = None

# Real IT department emails
IT_TEAM_EMAILS = [
    {
        'name': 'Ricardo Carmona',
        'email': 'ricardo.carmona@infinityairsprings.com',
        'role': 'Especialista de Redes (NETWORK)'
    },
    {
        'name': 'Fernando Herrera', 
        'email': 'fernando.herrera@infinityairsprings.com',
        'role': 'Gerente de TI'
    },
    {
        'name': 'Jesús Galindo',
        'email': 'jesus.galindo@infinityairsprings.com', 
        'role': 'Practicante de Redes y Soporte'
    }
]

def campaign_running():
    return running

def simulate_events():
    global running
    departments = get_departments()
    
    while running:
        time.sleep(random.randint(3, 10))  # Random interval between events
        
        if not running:
            break
            
        # Simulate events with focus on IT department and real emails
        department = random.choice(departments)
        action = random.choice(['clicked', 'ignored', 'reported'])
        
        # Use real IT emails when department is TI, otherwise simulate
        if department == 'TI':
            it_member = random.choice(IT_TEAM_EMAILS)
            email = it_member['email']
            print(f"IT Target: {it_member['name']} ({it_member['role']}) - {action}")
        else:
            email = f"user{random.randint(1, 50)}@infinityairsprings.com"
        
        # Simulate realistic IP addresses
        ip_address = f"192.168.{random.randint(1, 10)}.{random.randint(1, 254)}"
        
        record_event(department, action, email, ip_address)
        print(f"Event Recorded: {department} - {action} - {email}")

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