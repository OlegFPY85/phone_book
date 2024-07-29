import csv
import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Шаг 1: Приведение ФИО к правильному формату
for i in range(1, len(contacts_list)):
    full_name = " ".join(contacts_list[i][:3]).split()
    if len(full_name) == 2:
        contacts_list[i][0], contacts_list[i][1] = full_name[0], full_name[1]  # Фамилия, Имя
        contacts_list[i][2] = ''  # Отчество пустое
    elif len(full_name) == 3:
        contacts_list[i][0], contacts_list[i][1], contacts_list[i][2] = full_name  # ФИО
    else:
        contacts_list[i][0], contacts_list[i][1], contacts_list[i][2] = '', '', ''  # если нет ФИО

# Шаг 2: Форматирование телефонов
phone_pattern = re.compile(r'(\+7|8)?\s*[\(\-]?(\d{3})[\)\-\s]?(\d{3})[\-\s]?(\d{2})[\-\s]?(\d{2})(?:\s*доб\.(\d+))?')

def format_phone(phone):
    match = phone_pattern.fullmatch(phone)
    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(6):
            formatted_phone += f" доб.{match.group(6)}"
        return formatted_phone
    return phone  # если формат не распознан, возвращаем как есть

for i in range(1, len(contacts_list)):
    contacts_list[i][5] = format_phone(contacts_list[i][5])  # форматируем телефон

# Шаг 3: Объединение дублирующихся записей
unique_contacts = {}

for contact in contacts_list[1:]:
    key = f"{contact[0]} {contact[1]}"  # группируем по ФИ (Фамилия + Имя)
    if key not in unique_contacts:
        unique_contacts[key] = contact
    else:
        # Объединяем данные
        for j in range(len(contact)):
            if contact[j] and unique_contacts[key][j] == '':
                unique_contacts[key][j] = contact[j]

# Преобразуем уникальные контакты в список
contacts_list = list(unique_contacts.values())

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)
