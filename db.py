import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create tables for 'Powtórka z angielskiego' and 'Plan treningu'."""
    create_english_table = '''
    CREATE TABLE IF NOT EXISTS english_review (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        infinitive TEXT NOT NULL,
        past_simple TEXT NOT NULL,
        past_participle TEXT NOT NULL,
        translation TEXT NOT NULL
    );
    '''
    
    create_training_table = '''
    CREATE TABLE IF NOT EXISTS training_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_name TEXT NOT NULL,
        reps INTEGER NOT NULL,
        sets INTEGER NOT NULL,
        description TEXT
    );
    '''
    
    try:
        c = conn.cursor()
        c.execute(create_english_table)
        c.execute(create_training_table)
        conn.commit()
    except Error as e:
        print(e)

def insert_default_data(conn):
    """Insert predefined data directly into the tables."""
    english_data = [
        ("be", "was/were", "been", "być"),
        ("become", "became", "become", "stawać się"),
        ("begin", "began", "begun", "zaczynać"),
        ("break", "broke", "broken", "łamać"),
        ("bring", "brought", "brought", "przynosić")
    ]
    
    training_data = [
        ("Push-ups", 15, 3, "Pompki na klatkę piersiową"),
        ("Squats", 20, 3, "Przysiady na nogi"),
        ("Plank", 1, 3, "Deska na brzuch"),
        ("Burpees", 10, 3, "Dynamiczne ćwiczenie cardio"),
        ("Lunges", 12, 3, "Wykroki na nogi")
    ]
    
    try:
        c = conn.cursor()
        c.executemany('INSERT INTO english_review (infinitive, past_simple, past_participle, translation) VALUES (?, ?, ?, ?)', english_data)
        c.executemany('INSERT INTO training_plan (exercise_name, reps, sets, description) VALUES (?, ?, ?, ?)', training_data)
        conn.commit()
    except Error as e:
        print(e)

def show_data(conn, table_name):
    """Retrieve and display data from the specified table."""
    c = conn.cursor()
    if table_name == 'english_review':
        c.execute("SELECT * FROM english_review")
    elif table_name == 'training_plan':
        c.execute("SELECT * FROM training_plan")
    
    rows = c.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    db_file = 'database.db'
    
    # Connect to the database
    with create_connection(db_file) as conn:
        if conn is not None:
            # Create tables
            create_tables(conn)
            
            # Insert default data
            insert_default_data(conn)
            
            # Show data from both tables
            print("Powtórka z angielskiego:")
            show_data(conn, 'english_review')
            
            print("\nPlan treningu:")
            show_data(conn, 'training_plan')
        else:
            print("Error! Cannot create the database connection.")
