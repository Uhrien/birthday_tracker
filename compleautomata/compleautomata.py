import sqlite3
import requests
from datetime import datetime, timedelta
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

# Nuova funzione per ottenere i compleanni dei prossimi 7 giorni
def get_birthdays_next_7_days_with_group(db_path):
    today = datetime.now()
    next_week = today + timedelta(days=7)
    
    # Lista delle date nei prossimi 7 giorni nel formato "MM-DD"
    date_list = [(today + timedelta(days=i)).strftime("%m-%d") for i in range(1, 8)]

    # Connessione al database SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Creazione di una stringa di placeholder per la query
    placeholders = ','.join('?' for _ in date_list)

    # Esegui la query per ottenere i compleanni nei prossimi 7 giorni e il gruppo di appartenenza
    query = f'''
    SELECT persons.first_name, persons.last_name, groups.group_name, 
           strftime('%m-%d', REPLACE(persons.birthdate, '/', '-')) as birthday
    FROM persons
    JOIN persons_groups ON persons.id = persons_groups.person_id
    JOIN groups ON persons_groups.group_id = groups.id
    WHERE strftime('%m-%d', REPLACE(persons.birthdate, '/', '-')) IN ({placeholders})
    ORDER BY 
        CASE birthday
            {" ".join([f"WHEN '{date}' THEN {i}" for i, date in enumerate(date_list, start=1)])}
            ELSE 8
        END
    '''
    cursor.execute(query, date_list)

    # Recupera i risultati
    birthdays = cursor.fetchall()

    # Chiudi la connessione al database
    conn.close()

    return birthdays, date_list

# Funzione per inviare un messaggio tramite il bot Telegram
def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Opzionale: per formattare il messaggio con HTML
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
def send_today_birthdays(bot_token, chat_id, db_path):
    # Ottieni i compleanni odierni con il gruppo di appartenenza
    birthdays = get_birthdays_today_with_group(db_path)

    # Verifica se ci sono compleanni odierni e crea il messaggio
    if birthdays:
        for first_name, last_name, group_name in birthdays:
            message = f"🎉 Oggi è il compleanno di <b>{first_name} {last_name}</b> (<i>{group_name}</i>)"
            # Invia il messaggio al bot Telegram
            send_telegram_message(bot_token, chat_id, message)
    else:
        message = "Nessuno dei tuoi amici fa il compleanno oggi."
        # Invia il messaggio al bot Telegram
        send_telegram_message(bot_token, chat_id, message)

# Nuova funzione per inviare i compleanni dei prossimi 7 giorni con il gruppo
def send_next_7_days_birthdays(bot_token, chat_id, db_path):
    # Ottieni i compleanni nei prossimi 7 giorni con il gruppo di appartenenza
    birthdays, date_list = get_birthdays_next_7_days_with_group(db_path)

    # Organizza i compleanni per data
    birthdays_by_date = {date: [] for date in date_list}
    for first_name, last_name, group_name, birthday in birthdays:
        birthdays_by_date[birthday].append((first_name, last_name, group_name))

    # Crea il messaggio
    message_lines = ["🎂 **Compleanni nei prossimi 7 giorni:**"]
    for date in date_list:
        day = datetime.strptime(date, "%m-%d").strftime("%d %B")
        if birthdays_by_date[date]:
            for first_name, last_name, group_name in birthdays_by_date[date]:
                message_lines.append(f"• <b>{first_name} {last_name}</b> (<i>{group_name}</i>) - {day}")
        else:
            message_lines.append(f"• Nessun compleanno il {day}.")

    message = "\n".join(message_lines)

    # Invia il messaggio al bot Telegram
    send_telegram_message(bot_token, chat_id, message)

# Funzione principale per inviare i compleanni odierni e dei prossimi 7 giorni
def send_birthdays(bot_token, chat_id, db_path):
    send_today_birthdays(bot_token, chat_id, db_path)
    send_next_7_days_birthdays(bot_token, chat_id, db_path)

# Esegui lo script
if __name__ == "__main__":
    # Percorsi del database
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'birthday_tracker.db')

    # Token del bot Telegram e chat ID
    bot_token = 'INSERISCI IL TUO BOT TOKEN'
    chat_id = 'INSERISCI IL TUO CHAT IT'

    send_birthdays(bot_token, chat_id, db_path)
