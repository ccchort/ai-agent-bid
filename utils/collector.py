import json
from datetime import datetime
from zoneinfo import ZoneInfo


def correct_data(previus_data: dict, send_data: list, sender_type, final_name) -> list[dict]:

    if not send_data:
        return []

    result = []

    for item in send_data:
        bid = {
                    "Отметка времени": None,
                    "Дата (образец 27.04.2026)": None,
                    "Канал обращения клиента": None,
                    "От кого поступил запрос": None,
                    "Обращение": None,
                    "Документы": None,
                    "Приоритет выполнения задачи для исполнителя": None,
                    "Наименование клиента": None,
                    "Столбец 8": None,
                    "Отметка о постановки задачи": False,
                    "Ссылка на задачу в битрикс": None
                }

        true_date = datetime.fromisoformat(previus_data.get("created_at", None))
        bid["Отметка времени"] = true_date.strftime("%d.%m.%Y %H:%M:%S")
        bid["Дата (образец 27.04.2026)"] = true_date.strftime("%d.%m.%Y")
        bid["Канал обращения клиента"] = previus_data.get("platform", None)
        bid["От кого поступил запрос"] = sender_type
        bid["Обращение"] = item.get("Обращение", "Не обработано")
        bid["Документы"] = item.get("Документы", "")
        bid["Приоритет выполнения задачи для исполнителя"] = item.get("Приоритет выполнения задачи для исполнителя", "Нет")
        bid["Наименование клиента"] = final_name

        result.append(bid)

    return result

def format_datetime(value):
    if value is None:
        return None
    return value.astimezone(ZoneInfo("Europe/Samara")).strftime("%Y-%m-%d %H:%M:%S %z")