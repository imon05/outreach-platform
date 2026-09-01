import sqlite3

DB_FILE = "sudohumanx_outreach.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prospects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            username TEXT,
            profile_link TEXT,
            bio TEXT,
            pitch TEXT,
            timestamp DATETIME DEFAULT (datetime('now', '+5 hours', '30 minutes'))
        )
    ''')
    conn.commit()
    conn.close()

def save_prospects(prospects):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for p in prospects:
        c.execute('''
            INSERT INTO prospects (platform, username, profile_link, bio, pitch)
            VALUES (?, ?, ?, ?, ?)
        ''', (p['platform'], p['username'], p['profile_link'], p['bio'], p.get('pitch', '')))
    conn.commit()
    conn.close()
