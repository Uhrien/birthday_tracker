import os
import sqlite3
import pandas as pd

def setup_database():
    # Ottieni il percorso assoluto della directory corrente
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'birthday_tracker.db')

    # Connessione al database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Creazione della tabella 'persons' se non esiste
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        birthdate TEXT
    )
    ''')

    # Creazione della tabella 'persons_groups' se non esiste
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS persons_groups (
        person_id INTEGER,
        group_id INTEGER,
        person_full_name TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id)
    )
    ''')

    # Conferma delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()

def populate_persons_table():
    # Ottieni il percorso assoluto della directory corrente
    base_path = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_path, 'Compleanni.xlsx')
    db_path = os.path.join(base_path, 'birthday_tracker.db')

    # Leggi il file Excel
    df = pd.read_excel(excel_path)

    # Connessione al database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Inserisci i dati nella tabella 'persons' e aggiorna 'persons_groups'
    for _, row in df.iterrows():
        # Inserimento del record nella tabella 'persons'
        cursor.execute('''
        INSERT INTO persons (first_name, last_name, birthdate)
        VALUES (?, ?, ?)
        ''', (row['first_name'], row['last_name'], row['birthday']))

        # Recupero dell'ID del record appena inserito
        person_id = cursor.lastrowid

        # Creazione del full name
        person_full_name = f"{row['first_name']} {row['last_name']}"

        # Inserimento del record nella tabella 'persons_groups'
        cursor.execute('''
        INSERT INTO persons_groups (person_id, group_id, person_full_name)
        VALUES (?, ?, ?)
        ''', (person_id, 1, person_full_name))  # 'group_id' è impostato su 1 come esempio

    # Conferma delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()

    print("Dati inseriti nella tabella 'persons' e 'persons_groups' con successo!")

# Configurazione del database e popolamento delle tabelle
if __name__ == "__main__":
    setup_database()
    populate_persons_table()
