import sqlite3

def init_db():
    conn = sqlite3.connect('skin_kare.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            diagnosis TEXT,
            treatment TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the database
init_db()
