import requests

# Не забудь здесь поменять адрес
# На адрес своего сервера...
API_URL = "http://127.0.0.1:8000/solve"

with open("captcha.png", "rb") as image:
    response = requests.post(
        API_URL,
        files={"file": image}
    )

data = response.json()

print("\n" + "=" * 40)
print("          BARE API PROXY")
print("=" * 40)

if data.get("success"):
    print("[+] Статус: Успешно")
    print(f"[+] ID капчи: {data.get('captcha_id')}")
    print(f"[+] Ответ: {data.get('result')}")
else:
    print("[-] Статус: Ошибка")
    print(f"[-] Причина: {data.get('error', 'Неизвестная ошибка')}")

print("=" * 40)