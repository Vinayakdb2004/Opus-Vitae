import sqlite3


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(db_file, check_same_thread=False)  # Allow access from different threads
    return conn

def create_table(conn):
    """Create a table for users if it doesn't exist."""
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_users_table)
    except Exception as e:
        print(e)

# Other functions remain unchanged...

def add_user(conn, username, password):
    """Add a new user to the database."""
    sql = ''' INSERT INTO users(username, password) VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (username, password))
    conn.commit()
    return cur.lastrowid

def get_user(conn, username):
    """Retrieve a user by username."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    return cur.fetchone()
