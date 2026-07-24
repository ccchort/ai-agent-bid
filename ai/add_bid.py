import asyncio
import json
import traceback
from yandex_ai_studio_sdk import AsyncAIStudio
from config import config

from ai.info.clients import clients_list, partners_list


async def generate(data: dict) -> list[dict]:
    """
    Генерирует структурированные данные для CRM на основе накопленных сообщений пользователя.
    Если в одном накопленном потоке есть несколько независимых заявок,
    функция возвращает список словарей для всех заявок.

    :param data: dict, словарь с данными пользователя
    :return: list[dict]
    """
    sdk = AsyncAIStudio(
        folder_id=config.ai_folder_id.get_secret_value(),
        auth=config.ai_api_key.get_secret_value()
    )

    sdk.setup_default_logging()
    model = sdk.chat.completions('yandexgpt-5-lite')

    context = [
        {
            'role': 'system',
            'text': (
                'Ты — умный ассистент по обработке входящих заявок. '
                'Твоя задача — проанализировать накопленный массив сообщений от одного пользователя '
                'и определить, содержит ли он одну или несколько независимых заявок. '
                'Если в сообщениях есть несколько разных запросов, раздели их на отдельные заявки и '
                'верни список объектов JSON — по одному объекту на одну заявку. '
                'Если это одна заявка, верни список из одного объекта. '
                'Для каждой заявки извлеки следующую информацию: '
                'Дата и время, канал связи с клиентом, кто подал заявку, текст обращения, '
                'документы (если есть, обычно это ссылка на Google документ), наименование клиента(это название чата, в нем всегда содержится наименование, просто вытащи из названия), '
                'приоритет выполнения задачи для исполнителя, столбец 8 оставляй пустым(""), '
                'отметка о постановке задачи, ссылка на задачу в битрикс (тоже оставляй пустым ""). '
                'Если какой-то информации нет в сообщениях, оставь соответствующее поле пустым. '
                'Особенно важно для поля "От кого поступил запрос": '
                'если название клиента из названия чата совпадает с элементами из списка клиентов, ставь "Клиент"; '
                'если совпадает с элементами из списка партнеров, ставь "Партнер"; '
                'если нет совпадений, оставляй поле пустым. '
                'При сравнении учитывай, что в чатах названия могут быть без юридического статуса (ООО, ИП и т.д.), поэтому сравнивай по смыслу и по похожим названиям. '
                f'Список клиентов: {", ".join(clients_list)}. '
                f'Список партнеров: {", ".join(partners_list)}. '
                'Используй эти списки как справочник для определения типа. '
                'Не объединяй разные заявки в одну. Не придумывай данные. '
                'Возвращай только валидный JSON.'
            )
        },
        {
            'role': 'user',
            'text': (
                f"Вот накопленные сообщения: {data.get('accumulated_text')}\n"
                f"Вот наименование клиента: {data.get('client_name')}\n"
                f"Вот канал связи с клиентом: {data.get('platform')}\n"
                f"Вот дата и время обращения: {data.get('created_at')}\n"
                f"Вот отметка о постановке задачи: false"
            )
        },
    ]

    model = model.configure(response_format={
        "name": "crm_bid_list",
        "json_schema": {
            "title": "crm_bid_list",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "Отметка времени": {"title": "Отметка времени", "type": "string"},
                    "Дата (образец 27.04.2026)": {"title": "Дата (образец 27.04.2026)", "type": "string"},
                    "Канал обращения клиента": {"title": "Канал обращения клиента", "type": "string"},
                    "От кого поступил запрос": {"title": "От кого поступил запрос", "type": "string"},
                    "Обращение": {"title": "Обращение", "type": "string"},
                    "Документы": {"title": "Документы", "type": "string"},
                    "Приоритет выполнения задачи для исполнителя": {"title": "Приоритет выполнения задачи для исполнителя", "type": "string"},
                    "Наименование клиента": {"title": "Наименование клиента", "type": "string"},
                    "Столбец 8": {"title": "Столбец 8", "type": "string"},
                    "Отметка о постановки задачи": {"title": "Отметка о постановки задачи", "type": "boolean"},
                    "Ссылка на задачу в битрикс": {"title": "Ссылка на задачу в битрикс", "type": "string"}
                },
                "required": [
                    "Отметка времени",
                    "Дата (образец 27.04.2026)",
                    "Канал обращения клиента",
                    "От кого поступил запрос",
                    "Обращение",
                    "Документы",
                    "Приоритет выполнения задачи для исполнителя",
                    "Наименование клиента",
                    "Столбец 8",
                    "Отметка о постановки задачи",
                    "Ссылка на задачу в битрикс"
                ]
            }
        }
    })

    try:
        result = await model.run(context)
    except Exception:
        print("AI SDK exception traceback:")
        traceback.print_exc()
        return []

    if not result or not getattr(result, 'text', None):
        print("AI SDK returned empty result")
        return []

    try:
        payload = json.loads(result.text)
    except json.JSONDecodeError as e:
        print("AI JSON decode error:", e)
        print("AI raw text:", str(result.text)[:1000])
        return []

    if isinstance(payload, dict):
        payload = [payload]

    if isinstance(payload, list) and len(payload) == 1 and isinstance(payload[0], dict):
        return [payload[0]]

    return payload

    

# Запуск асинхронного цикла
if __name__ == "__main__":
    result = asyncio.run(generate({'id': 16, 'user_id': 1414952718, 'platform': 'Telegram', 'accumulated_text': 'привет, нужно оплатить счет а совсем забыл что еще нужно проверить ревизиты у клиентов', 'created_at': '2026-07-21 22:33:05 +0400', 'last_message_at': '2026-07-21 22:44:33 +0400', 'client_name': 'Егор'}))
    print(result)
