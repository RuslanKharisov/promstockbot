import re
from typing import Optional


def extract_phone(text: str) -> Optional[str]:
    """
    Извлекает российский телефонный номер в форматах:
    - 8XXXXXXXXXX (11 цифр)
    - +7XXXXXXXXXX (11 цифр)
    - 7XXXXXXXXXX (11 цифр, без +)

    Возвращает номер в международном формате (+7...)
    или None, если номер не найден.
    """
    phone_match = re.search(
        r'(?:\+7|7|8)(?:\s*\d\s*){10}',  # Ищем +7/7/8 и 10 цифр (с возможными пробелами)
        text
    )

    if phone_match:
        phone = re.sub(r'[^\d]', '', phone_match.group(0))  # Удаляем все нецифровые символы
        if phone.startswith('8'):
            return '+7' + phone[1:]  # Конвертируем 8... в +7...
        elif phone.startswith('7'):
            return '+' + phone  # Добавляем + к 7...
        return phone  # Для случаев, если номер уже в формате +7...
    return None


def extract_email(text: str) -> Optional[str]:
    """
    Извлекает email адрес с улучшенной валидацией:
    - Поддержка Unicode символов (например, кириллица)
    - Проверка валидности доменной части
    - Игнорирует частичные совпадения в середине строки
    """
    email_match = re.search(
        r'(?<![\w@.+-])(?:[a-zA-Z0-9а-яА-Я_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,})(?![\w@.+-])',
        text,
        re.IGNORECASE
    )
    return email_match.group(0) if email_match else None


# Примеры использования:
if __name__ == '__main__':
    test_text = """
    Контакты: example@mail.com, 8 (495) 123-45-67, 
    +7 999 123-45-67, 74951234567, not-an-email@invalid
    """

    print(extract_phone(test_text))  # +74951234567
    print(extract_email(test_text))  # example@mail.com
