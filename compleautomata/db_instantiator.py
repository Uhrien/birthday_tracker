import sqlite3

# Connessione al database (verrà creato se non esiste)
conn = sqlite3.connect('birthday_tracker.db')
cursor = conn.cursor()

# Creazione tabella 'persons'
cursor.execute('''
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    birthdate TEXT
)
''')

# Creazione tabella 'groups'
cursor.execute('''
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT
)
''')

# Creazione tabella 'persons_groups'
cursor.execute('''
CREATE TABLE IF NOT EXISTS persons_groups (
    person_id INTEGER,
    group_id INTEGER,
    person_full_name TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
)
''')

# Conferma delle modifiche e chiusura della connessione
conn.commit()
conn.close()

print("Database e tabelle creati con successo!")
