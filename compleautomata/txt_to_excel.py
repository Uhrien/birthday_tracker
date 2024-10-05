import re
import pandas as pd

# Funzione per convertire la data nel formato "YYYY/MM/DD"
def convert_date(date_str):
    month_map = {
        'Gennaio': '01', 'Febbraio': '02', 'Marzo': '03',
        'Aprile': '04', 'Maggio': '05', 'Giugno': '06',
        'Luglio': '07', 'Agosto': '08', 'Settembre': '09',
        'Ottobre': '10', 'Novembre': '11', 'Dicembre': '12'
    }
    day, month = date_str.split()
    month_number = month_map[month]
    return f"1990/{month_number}/{int(day):02d}"

# Lettura del file di testo
with open('Compleanni.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

data = []
pattern = r"(\d{1,2} \w+) -> (.+)"

# Parsing del file di testo
for line in lines:
    match = re.match(pattern, line.strip())
    if match:
        date_str = match.group(1)
        full_name = match.group(2)
        first_name, last_name = full_name.rsplit(' ', 1)
        converted_date = convert_date(date_str)
        data.append([first_name, last_name, converted_date])

# Creazione di un DataFrame con ID incrementale e colonne richieste
df = pd.DataFrame(data, columns=['first_name', 'last_name', 'birthday'])
df.insert(0, 'id', range(1, len(df) + 1))

# Salvataggio in un file Excel
output_path = "Compleanni.xlsx"
df.to_excel(output_path, index=False)

print(f"File Excel '{output_path}' creato con successo!")
