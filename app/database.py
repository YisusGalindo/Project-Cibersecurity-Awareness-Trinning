import sqlite3

def init_db():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS events (action TEXT)")
    conn.commit()
    conn.close()

def record_event(action):
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("INSERT INTO events VALUES (?)", (action,))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    actions = ['clicked', 'ignored', 'reported']
    result = {action: 0 for action in actions}
    for action in actions:
        c.execute("SELECT COUNT(*) FROM events WHERE action=?", (action,))
        result[action] = c.fetchone()[0]
    conn.close()
    return result

init_db()