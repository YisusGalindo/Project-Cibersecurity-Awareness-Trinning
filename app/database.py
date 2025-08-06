import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    # Create events table with more detailed information
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        email TEXT,
        ip_address TEXT
    )''')
    
    # Create departments table
    c.execute('''CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        email_template TEXT,
        target_count INTEGER DEFAULT 0
    )''')
    
    # Create campaigns table
    c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_time DATETIME,
        end_time DATETIME,
        status TEXT DEFAULT 'stopped'
    )''')
    
    # Insert default departments
    departments = [
        ('TI', 'ti_template.html'),
        ('LOGISTICA', 'logistica_template.html'),
        ('FINANZAS', 'finanzas_template.html'),
        ('COMPRAS', 'compras_template.html'),
        ('CUSTOMER SERVICE', 'customer_service_template.html'),
        ('SEGURIDAD E HIGIENE', 'seguridad_template.html'),
        ('PRODUCCIÓN', 'produccion_template.html'),
        ('MANTENIMIENTO', 'mantenimiento_template.html'),
        ('RH', 'rh_template.html'),
        ('EMBARQUE', 'embarque_template.html'),
        ('ALMACÉN', 'almacen_template.html'),
        ('CALIDAD', 'calidad_template.html'),
        ('RECIBO', 'recibo_template.html')
    ]
    
    for dept_name, template in departments:
        c.execute("INSERT OR IGNORE INTO departments (name, email_template) VALUES (?, ?)", 
                 (dept_name, template))
    
    conn.commit()
    conn.close()

def record_event(department, action, email=None, ip_address=None):
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (department, action, email, ip_address) VALUES (?, ?, ?, ?)", 
             (department, action, email, ip_address))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    # Get overall stats
    actions = ['clicked', 'ignored', 'reported']
    result = {action: 0 for action in actions}
    
    for action in actions:
        c.execute("SELECT COUNT(*) FROM events WHERE action=?", (action,))
        result[action] = c.fetchone()[0]
    
    # Get stats by department
    c.execute("SELECT name FROM departments")
    departments = [row[0] for row in c.fetchall()]
    
    dept_stats = {}
    for dept in departments:
        dept_stats[dept] = {}
        for action in actions:
            c.execute("SELECT COUNT(*) FROM events WHERE department=? AND action=?", (dept, action))
            dept_stats[dept][action] = c.fetchone()[0]
    
    result['by_department'] = dept_stats
    result['departments'] = departments
    
    conn.close()
    return result

def get_departments():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("SELECT name FROM departments")
    departments = [row[0] for row in c.fetchall()]
    conn.close()
    return departments

def start_campaign_db():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("INSERT INTO campaigns (name, start_time, status) VALUES (?, ?, ?)", 
             ("Campaign " + datetime.now().strftime("%Y-%m-%d %H:%M"), datetime.now(), "running"))
    conn.commit()
    conn.close()

def stop_campaign_db():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("UPDATE campaigns SET end_time=?, status=? WHERE status='running'", 
             (datetime.now(), "stopped"))
    conn.commit()
    conn.close()

init_db()