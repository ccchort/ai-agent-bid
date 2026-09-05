def make_message_to_managers(data: dict) -> str:
    """
    Приводит список словарей с обращениями в текст сообщения менеджерам.

    :param data: list, список обращений 
    """

    text = ""
    text += f"Появились новые обращения: {len(data)}\n\n"
    for index, bid in enumerate(data):
        text += f"<i>Обращение {index + 1}</i>\n"\
        f"<b>Клиент и канал связи</b>: {bid.get("Наименование клиента", "Неизвестно")}; {bid.get("Канал обращения клиента")}\n"\
        f"<b>Приоритет</b>: {bid.get("Приоритет выполнения задачи для исполнителя", "Неизвестно")}\n"\
        f"<b>Обращение</b>: <blockquote>{bid.get("Обращение", "")}</blockquote>\n\n"

    return text
