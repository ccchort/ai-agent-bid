import gspread

def insert_row_to_google_sheet(data, json_key_path, spreadsheet_name, worksheet_name="Ответы на форму (1)"):
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
    
    # Строгое соответствие колонок структуре
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

        sheet.append_row(row_data, value_input_option="USER_ENTERED")
    print(f"Данные успешно добавлены: {len(rows)} строк!")



# --- Пример использования ---
# my_data = {
#     "Отметка времени": "04-07-2026 17:56:24.289",
#     "Дата": "04.07.2026",
#     "Канал обращения клие": "Max",
#     "От кого поступил запрc": "Клиент",
#     "Обращение": "оплатить счет",
#     "Документы": "Не указано",
#     "Приоритет": "Нет",
#     "Наименов": "Егор",
#     "Отметка о постановки задачи": False,
#     "Ссылка на": ""
# }
# insert_row_to_google_sheet(my_data, "credentials.json", "Название_Таблицы")
