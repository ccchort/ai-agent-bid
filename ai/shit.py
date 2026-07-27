import asyncio

import gspread
from gspread.utils import ValueInputOption

async def insert_row_to_google_sheet(data, json_key_path, spreadsheet_name, worksheet_name="Ответы ИИ"):
    """
    Принимает один словарь или список словарей с данными и вставляет их в Google Таблицу.

    :param data: dict | list[dict], данные для вставки
    :param json_key_path: str, путь к вашему JSON-файлу с ключами от Google Cloud
    :param spreadsheet_name: str, название вашей Google Таблицы
    :param worksheet_name: str, название конкретного листа
    """

    if not data:
        return

    if isinstance(data, dict):
        rows = [data]
    else:
        rows = data

    client = gspread.service_account(filename=json_key_path)
    
    # Открытие таблицы и листа
    sheet = client.open(spreadsheet_name).worksheet(worksheet_name)

    start_row = len(sheet.get_all_values()) + 1
    # Строгое соответствие колонок структуре
    formatted_rows = []
    for data_dict in rows:
        row_data = [
            data_dict.get("Отметка времени", ""),
            data_dict.get("Дата (образец 27.04.2026)", ""),
            data_dict.get("Канал обращения клиента", ""),
            data_dict.get("От кого поступил запрос", ""),
            data_dict.get("Обращение", ""),
            data_dict.get("Документы", ""),
            data_dict.get("Приоритет выполнения задачи для исполнителя", ""),
            data_dict.get("Наименование клиента", ""),
            data_dict.get("Столбец 8", ""),
            data_dict.get("Отметка о постановки задачи", False),
            data_dict.get("Ссылка на задачу в битрикс", "")
        ]
        formatted_rows.append(row_data)

    sheet.insert_rows(values=formatted_rows, row=start_row, value_input_option=ValueInputOption.raw, inherit_from_before=True)



    print(f"Данные успешно добавлены: {len(rows)} строк!")



my_data = [{'Отметка времени': '27.07.2026 14:33:19', 'Дата (образец 27.04.2026)': '27.07.2026', 'Канал обращения клиента': 'Telegram', 'От кого поступил запрос': 'Клиент', 'Обращение': 'А номер наш же должен быть', 'Документы': '', 'Приоритет выполнения задачи для исполнителя': 'Нет', 'Наименование клиента': 'Автопрайм ООО', 'Столбец 8': None, 'Отметка о постановки задачи': False, 'Ссылка на задачу в битрикс': None}]

if __name__ == "__main__":
    asyncio.run(insert_row_to_google_sheet(my_data, "./ai/info/bids-project-502021-d03d48f79611.json", "Регистрация обращений клиентов (Ответы)"))