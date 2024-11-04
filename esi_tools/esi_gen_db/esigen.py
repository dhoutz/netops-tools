import sqlite3
import random
import os

def generate_unique_esi():
    # Generate a 10-tuple ESI, starting with '00:'
    esi_parts = [0]  # Start with 00
    esi_parts += [random.randint(0, 255) for _ in range(9)]  # Generate the remaining 9 bytes
    # Format the ESI as a string with colons between every two characters
    esi = ':'.join(format(part, '02x') for part in esi_parts)
    return esi

def create_database(db_name):
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table for storing ESIs if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evpn_esi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            esi TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    return conn

def store_esi(conn, esi):
    cursor = conn.cursor()
    try:
        # Insert the unique ESI into the database
        cursor.execute('INSERT INTO evpn_esi (esi) VALUES (?)', (esi,))
        conn.commit()
        print(f'Successfully stored ESI: {esi}')
    except sqlite3.IntegrityError:
        print(f'ESI {esi} already exists in the database.')

def main():
    db_name = 'evpn_esi.db'
    
    # Check if the database file exists
    db_exists = os.path.exists(db_name)

    if db_exists:
        conn = sqlite3.connect(db_name)
    else:
        conn = create_database(db_name)
    
    # Generate and store a unique ESI
    esi = generate_unique_esi()
    store_esi(conn, esi)
   
    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()
