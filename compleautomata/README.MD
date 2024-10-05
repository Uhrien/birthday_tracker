********************************
*******COMPLEAUTOMATA Bot*******
********************************

Questo progetto è uno script Python che interagisce con un database SQLite per trovare le persone che festeggiano il compleanno nella data odierna e inviare un messaggio tramite un bot Telegram. Lo script è stato progettato per essere eseguito automaticamente ogni giorno tramite un cron job su un Raspberry Pi Zero 2 W su Raspibian OS Lite.

Struttura del Database
Il database SQLite, chiamato birthday_tracker.db, contiene tre tabelle:

1. persons
Questa tabella contiene le informazioni sulle persone, tra cui il nome e la data di nascita.

id (INTEGER PRIMARY KEY AUTOINCREMENT): ID unico per ogni persona.
first_name (TEXT): Nome della persona.
last_name (TEXT): Cognome della persona.
birthdate (TEXT): Data di nascita della persona nel formato YYYY/MM/DD.

2. groups
Questa tabella contiene i gruppi a cui le persone possono appartenere.

id (INTEGER PRIMARY KEY AUTOINCREMENT): ID unico per ogni gruppo.
group_name (TEXT): Nome del gruppo.

3. persons_groups
Questa è una tabella associativa che collega le persone ai gruppi.

person_id (INTEGER): ID della persona (collegato alla tabella persons).
group_id (INTEGER): ID del gruppo (collegato alla tabella groups).
person_full_name (TEXT): Nome completo della persona (in formato first_name last_name, per avere un riferimento grafico in tabella della persona).


*******************
**** OPZIONALE ****
*******************

Un esempio di file txt potrebbe essere così composto:
"
COMPLEANNI:

5  Gennaio -> Cosimo Cozzoli
21 Gennaio -> Vito Liantonio

15 Dicembre -> Daniela Porretto
15 Dicembre -> Nicola Morotti
"

Per trasformarlo in excel ho usato lo script txt_to_excel.py
Successivamente ho usato lo script excel_to_db.py per popolare la tabella persons su db.


NB: Per instanziare il Database da zero ed impostarlo come nella descrizione precedente ho creato uno script chiamato db_instantiator.py
Per popolarlo ho usato un file txt compilato negli anni, che ho poi trasformato in excel, che ho infine usato per popolare almeno la tabella persons.


********************************
***Funzionamento dello Script***
********************************

Descrizione

Lo script compleautomata.py esegue una query sul database per trovare tutte le persone che festeggiano il compleanno oggi e invia un messaggio Telegram per ciascun compleanno trovato.

Funzionamento:
Connessione al Database:

Lo script si connette al database SQLite (birthday_tracker.db).
Ricerca Compleanni Odierni:

Utilizza una query SQL per cercare tutte le persone il cui compleanno cade nella data odierna. Il controllo viene fatto solo sul giorno e mese, ignorando l'anno.
Invio Messaggio Tramite Bot Telegram:

Utilizza l'API di Telegram per inviare un messaggio con i dettagli dei compleanni odierni.
Il messaggio include il nome e il gruppo di appartenenza di ogni persona.
Automatizzazione con Cron Job:

Lo script può essere eseguito automaticamente ogni giorno alle 6:00 del mattino utilizzando un cron job.

Esecuzione Manuale dello Script
Per eseguire manualmente lo script supponendo che si trovi in /home/scripts/:

python3 /home/scripts/compleautomata.py
Installazione del Cron Job
Per far eseguire lo script ogni giorno alle 6:00 del mattino, puoi aggiungere una voce nel crontab:

Apri il crontab con:

crontab -e

Aggiungi la seguente riga alla fine del file:

0 6 * * * /usr/bin/python3 /home/scripts/compleautomata.py

Questo farà in modo che lo script venga eseguito automaticamente ogni giorno alle 6:00 AM.

Requisiti:
Python 3.
Libreria Requests per inviare messaggi all'API di Telegram.

(Puoi installarla con il comando:   pip install requests)
SQLite per gestire il database dei compleanni.

Configurazione del Bot Telegram
Lo script utilizza un bot Telegram per inviare notifiche. Per configurare il bot:

Crea un bot Telegram utilizzando BotFather.

Ottieni il bot token e inseriscilo nello script (te lo fornisce BotFather quando crei il bot).
Ottieni il chat ID per la chat/gruppo dove vuoi inviare il messaggio.

Variabili da Configurare:

bot_token: Inserisci il token del bot Telegram.
    NB: Per ottenere il l'API Token (o bot token) basta creare il Bot, seguire il wizard di BotFather su telegram e alla fine del procedimento BotFather ti invierà un messaggio contenente tra le altre info, anche L'API TOKEN.
chat_id: Inserisci il chat ID della chat o del gruppo a cui inviare i messaggi.
    NB: Per ottenere il chat id puoi farlo andando a questo URL: https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/getUpdates. Poi aprendo il bot telegram sulla tua app/webapp di telegram scrivi qualcosa e ricarica l'url di prima. Questo avrà un payload con all'interno il chat id.
    


Esempio di Output
Se oggi è il 15 Dicembre, e ci sono due persone (Daniela Porretto e Nicola Morotti) nel database con il compleanno il 15/12, il bot invierà i seguenti messaggi:

🎉 Oggi è il compleanno di Daniela Porretto (Famiglia)
🎉 Oggi è il compleanno di Nicola Morotti (Lavoro)