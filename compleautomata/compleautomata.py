import sqlite3
import requests
from datetime import datetime
import os

# Funzione per ottenere i compleanni odierni e il gruppo di appartenenza
def get_birthdays_today_with_group(db_path):
    # Ottieni la data odierna nel formato "MM-DD"
    today = datetime.now().strftime("%m-%d")

    # Connessione al database SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Esegui la query per ottenere i compleanni odierni e il gruppo di appartenenza
    cursor.execute('''
    SELECT persons.first_name, persons.last_name, groups.group_name 
    FROM persons
    JOIN persons_groups ON persons.id = persons_groups.person_id
    JOIN groups ON persons_groups.group_id = groups.id
    WHERE strftime('%m-%d', REPLACE(persons.birthdate, '/', '-')) = ?
    ''', (today,))

    # Recupera i risultati
    birthdays = cursor.fetchall()

    # Chiudi la connessione al database
    conn.close()

    return birthdays

# Funzione per inviare un messaggio tramite il bot Telegram
def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()  # Solleva un'eccezione per codici di stato HTTP non 200-299
        print("Messaggio inviato con successo!")
    except requests.exceptions.Timeout:
        print("Errore: Timeout durante la connessione all'API di Telegram.")
    except requests.exceptions.ConnectionError as e:
        print("Errore: Problema di connessione:", e)
    except requests.exceptions.HTTPError as e:
        print("Errore HTTP:", e)
    except requests.exceptions.RequestException as e:
        print("Errore durante l'invio del messaggio:", e)

# Funzione principale per inviare i compleanni odierni con il gruppo
def send_today_birthdays():
    # Percorsi del database
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'birthday_tracker.db')

    # Token del bot Telegram e chat ID
    bot_token = 'API_TOKEN'
    chat_id = 'CHAT_ID'

    # Ottieni i compleanni odierni con il gruppo di appartenenza
    birthdays = get_birthdays_today_with_group(db_path)

    # Verifica se ci sono compleanni odierni e crea il messaggio
    if birthdays:
        for first_name, last_name, group_name in birthdays:
            message = f"🎉 Oggi è il compleanno di {first_name} {last_name} ({group_name})"
            # Invia il messaggio al bot Telegram
            send_telegram_message(bot_token, chat_id, message)
    else:
        message = "Nessuno ha il compleanno oggi."
        # Invia il messaggio al bot Telegram
        send_telegram_message(bot_token, chat_id, message)

# Esegui lo script
if __name__ == "__main__":
    send_today_birthdays()
