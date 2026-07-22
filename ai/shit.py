import gspread

def insert_row_to_google_sheet(data_dict, json_key_path, spreadsheet_name, worksheet_name="Ответы на форму (1)"):
    """
    Принимает словарь с данными и вставляет его в Google Таблицу.
    
    :param data_dict: dict, данные для вставки (ключи должны совпадать со структурой колонок)
    :param json_key_path: str, путь к вашему JSON-файлу с ключами от Google Cloud
    :param spreadsheet_name: str, название вашей Google Таблицы
    :param worksheet_name: str, название конкретного листа (по умолчанию "Лист1")
    """

    client = gspread.service_account(filename=json_key_path)
    
    # Открытие таблицы и листа
    sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
    
    # Строгое соответствие колонок структуре на скриншоте
    row_data = [
        data_dict.get("Отметка времени", ""),
        data_dict.get("Дата (образец 27.04.2026)", ""),
        data_dict.get("Канал обращения клиента", ""), # Обрезано на скрине: "Канал обращения клиента"
        data_dict.get("От кого поступил запрос", ""), # Обрезано на скрине: "От кого поступил запрос"
        data_dict.get("Обращение", ""),
        data_dict.get("Документы", ""),
        data_dict.get("Приоритет выполнения задачи для исполнителя", ""),
        data_dict.get("Наименование клиента", ""), 
        data_dict.get("Столбец 8", ""),            # Обрезано на скрине: "Наименование"
        data_dict.get("Отметка о постановки задачи", False), # Чекбокс (True/False)
        data_dict.get("Ссылка на задачу в битрикс", "")             # Обрезано на скрине: "Ссылка на..."
    ]
    
    # Добавление строки в конец таблицы
    sheet.append_row(row_data, value_input_option="USER_ENTERED")
    print("Данные успешно добавлены!")



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
