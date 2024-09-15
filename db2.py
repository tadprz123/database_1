import sqlite3
import csv
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
    """Create tables for data from the CSV files."""
    create_stations_table = '''
    CREATE TABLE IF NOT EXISTS stations (
        station_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        elevation REAL
    );
    '''
    
    create_measurements_table = '''
    CREATE TABLE IF NOT EXISTS measurements (
        station_id TEXT,
        date TEXT,
        value REAL,
        measurement_type TEXT,
        PRIMARY KEY (station_id, date, measurement_type),
        FOREIGN KEY (station_id) REFERENCES stations (station_id)
    );
    '''
    
    try:
        c = conn.cursor()
        c.execute(create_stations_table)
        c.execute(create_measurements_table)
        conn.commit()
    except Error as e:
        print(e)

def insert_data_from_csv(conn, csv_file, table_name):
    """Insert data from a CSV file into the specified table."""
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            if table_name == 'stations':
                sql = '''INSERT INTO stations (station_id, name, latitude, longitude, elevation) 
                         VALUES (?, ?, ?, ?, ?)'''
                conn.execute(sql, (row[0], row[1], row[2], row[3], row[4]))
            elif table_name == 'measurements':
                sql = '''INSERT INTO measurements (station_id, date, value, measurement_type) 
                         VALUES (?, ?, ?, ?)'''
                conn.execute(sql, (row[0], row[1], row[2], row[3]))
        conn.commit()

def show_data(conn, table_name):
    """Retrieve and display data from the specified table."""
    c = conn.cursor()
    if table_name == 'stations':
        c.execute("SELECT * FROM stations")
    elif table_name == 'measurements':
        c.execute("SELECT * FROM measurements")
    
    rows = c.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    db_file = 'database2.db'
    
    # Podaj ścieżki do plików CSV
    stations_csv = 'clean_stations.csv'  # Upewnij się, że ten plik znajduje się w tym samym folderze co skrypt
    measurements_csv = 'clean_measure.csv'  # Analogicznie

    # Connect to the database
    with create_connection(db_file) as conn:
        if conn is not None:
            # Create tables
            create_tables(conn)
            
            # Insert data from CSV files
            insert_data_from_csv(conn, stations_csv, 'stations')
            insert_data_from_csv(conn, measurements_csv, 'measurements')
            
            # Show data from both tables
            print("Stacje pomiarowe:")
            show_data(conn, 'stations')
            
            print("\nPomiary:")
            show_data(conn, 'measurements')
        else:
            print("Error! Cannot create the database connection.")

