# BareAPI Proxy

Лёгкий прокси-сервер для Bare API на Python + FastAPI.

Принимает изображения через HTTP POST-запрос, отправляет их в Bare API, ожидает результат и возвращает его клиенту в формате JSON.

## Возможности

- ⚡ Асинхронная обработка запросов.
- 🔑 API-ключ хранится внутри `app.py`.
- 🖼️ Приём изображений через POST-запрос.
- 🔄 Автоматическое получение результата.
- 📦 JSON-ответы.
- ⏱️ Настраиваемый интервал проверки.
- 🐧 Поддержка Linux VPS/VDS.

## Структура проекта

```text
Bare-API-Proxy/
├── app.py
├── requirements.txt
└── README.md
```

## Установка

```bash
git clone https://github.com/SiberianHacker/Bare-API-Proxy.git
cd Bare-API-Proxy

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Настройка

Откройте `app.py` и укажите свой API-ключ:

```python
API_KEY = "ключ от Bare API"
```

## Запуск

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

По умолчанию сервер доступен на порту `8000`.

## Запуск в фоне

Для работы сервера после закрытия SSH-сессии:

```bash
nohup venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

Просмотр логов:

```bash
tail -f server.log
```

Остановка:

```bash
pkill -f "uvicorn app:app"
```

## API

### `POST /solve`

Отправляет изображение на обработку.

**Тип запроса:** `multipart/form-data`

| Параметр | Тип | Описание |
|---|---|---|
| `file` | File | Изображение |

### Пример запроса (Python)

```python
import requests

response = requests.post(
    "http://SERVER_IP:8000/solve",
    files={"file": open("image.png", "rb")}
)

print(response.json())
```

### Пример запроса (cURL)

```bash
curl -X POST http://SERVER_IP:8000/solve \
  -F "file=@image.png"
```

## Ответ API

**Успешный запрос:**

```json
{
    "success": true,
    "captcha_id": "8ad78c87-ae90-4d80-ab90-79d444d9f8cb",
    "result": "epjk"
}
```

**Ошибка:**

```json
{
    "success": false,
    "captcha_id": "123456789",
    "error": "Timeout: captcha not solved"
}
```

## Зависимости

- Python 3.9+
- FastAPI
- Uvicorn
- HTTPX
- Python Multipart

## Лицензия

MIT License.
