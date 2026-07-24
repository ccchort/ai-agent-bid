import re
from rapidfuzz import process, fuzz

def clean_for_matching(name: str) -> str:
    """
    Глубокая очистка строк ТОЛЬКО для сопоставления.
    Удаляет юр. лица, инициалы, слово 'бухгалтерия' и спецсимволы.
    """
    if not name:
        return ""
    
    name = name.lower()
    
    # 1. Удаляем слово 'бухгалтерия' и сопутствующий шум
    name = re.sub(r'\b(бухгалтерия|групп|группа|компания|фирма)\b', ' ', name)
    
    # 2. Удаляем организационные формы
    name = re.sub(r'\b(ип|ооо|зао|оао|гск|ooo|ltd|co|ано|до|удпо)\b', ' ', name)
    
    # 3. Удаляем одиночные инициалы (например: 'а.в.', 'н.н.', 'и.', 'а.')
    # Этот паттерн уберет 'а.в.', 'а. в.' и просто одиночные буквы ' а ' после удаления точек
    name = re.sub(r'\b[а-яa-z]\b\.?', ' ', name)
    
    # 4. Удаляем все спецсимволы и кавычки
    name = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', ' ', name)
    
    # Схлопываем пробелы
    return " ".join(name.split())

def match_company(client_name_from_chat: str, clients_list: list, partners_list: list) -> tuple:
    """
    Ищет совпадение названия чата со списками.
    Возвращает КОРТЕЖ: (Тип_отправителя, Оригинальное_название_из_списка)
    Если совпадений нет, возвращает ("", "")
    """
    cleaned_chat = clean_for_matching(client_name_from_chat)
    if not cleaned_chat:
        return "", ""
        
    # Создаем словари, где ключ — очищенное название, а значение — оригинал из вашего списка
    # Это позволит по очищенному тексту мгновенно вытащить оригинал с "ООО/ИП"
    cleaned_clients = {clean_for_matching(c): c for c in clients_list if clean_for_matching(c)}
    cleaned_partners = {clean_for_matching(p_orig): p_orig for p_orig in partners_list if (cleaned_p := clean_for_matching(p_orig))}
    
    # Настройки нечеткого поиска:
    # Используем fuzz.token_set_ratio — он идеален, когда слова перепутаны местами 
    # или когда в одной строке есть лишние слова (например, "летяева лейба сигма" vs "летяева")
    
    best_client_match = process.extractOne(
        cleaned_chat, 
        cleaned_clients.keys(), 
        scorer=fuzz.token_set_ratio, 
        score_cutoff=75 # Порог схожести (75% достаточно для коротких названий с перестановками)
    )
    
    best_partner_match = process.extractOne(
        cleaned_chat, 
        cleaned_partners.keys(), 
        scorer=fuzz.token_set_ratio, 
        score_cutoff=75
    )
    
    client_score = best_client_match[1] if best_client_match else 0
    partner_score = best_partner_match[1] if best_partner_match else 0
    
    # Если зацепки нет ни там, ни там
    if client_score == 0 and partner_score == 0:
        return "", ""
        
    # Возвращаем оригинал из того списка, где балл совпадения выше
    if client_score >= partner_score:
        matched_cleaned_name = best_client_match[0]
        original_name = cleaned_clients[matched_cleaned_name]
        return "Клиент", original_name
    else:
        matched_cleaned_name = best_partner_match[0]
        original_name = cleaned_partners[matched_cleaned_name]
        return "Партнер", original_name
