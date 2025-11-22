import sqlite3

DB_NAME = "study_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. SUBJECTS Table (Added pos_x, pos_y)
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT DEFAULT '#3498db',
        icon TEXT DEFAULT 'BOOK',
        schedule TEXT DEFAULT '',
        pos_x INTEGER DEFAULT 0,
        pos_y INTEGER DEFAULT 0
    )''')

    # 2. TASKS Table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'Todo',
        due_date TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
    )''')

    # 3. ATTACHMENTS Table
    c.execute('''CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        file_name TEXT,
        file_path TEXT,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )''')

    # --- PRE-POPULATE DATA ---
    c.execute("SELECT count(*) FROM subjects")
    if c.fetchone()[0] == 0:
        # Default positions (x, y) are 0, they will be auto-arranged by main.py on first run
        subjects_data = [
            ("Intro to Biology (ITB)", "#2ecc71", "BIOTECH", "24/11 (3pm - 6pm)"),
            ("Algo Analysis (AAD)",    "#3498db", "CODE",    "27/11 (3pm - 6pm)"),
            ("Probability (PRP)",      "#9b59b6", "TIMELINE","28/11 (3pm - 6pm)"),
            ("Data & Apps (DnA)",      "#e67e22", "STORAGE", "29/11 (3pm - 6pm)"),
            ("Quantum Mech (QM)",      "#34495e", "SCIENCE", "1/12 (9am - 12pm)")
        ]
        c.executemany("INSERT INTO subjects (name, color, icon, schedule) VALUES (?, ?, ?, ?)", subjects_data)
        print("Database initialized!")

    conn.commit()
    conn.close()

def update_subject_position(subject_id, x, y):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE subjects SET pos_x = ?, pos_y = ? WHERE id = ?", (int(x), int(y), subject_id))
    conn.commit()
    conn.close()

def get_subjects():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM subjects")
    rows = c.fetchall()
    conn.close()
    return rows

def add_task(title, subject_id=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, status, subject_id) VALUES (?, 'Todo', ?)", (title, subject_id))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
