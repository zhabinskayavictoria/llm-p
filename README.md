# Построение защищённого API для работы с большой языковой моделью 

FastAPI сервис с JWT-аутентификацией, SQLite и проксированием запросов к LLM через OpenRouter

# Установка и запуск 
### Установка uv
```
pip install uv
```

### Создание и активация виртуального окружения
```
uv venv
source .venv/bin/activate # MacOS/Linux
.venv\Scripts\activate.bat # Windows
```

### Установка зависимостей
```
uv pip install -r <(uv pip compile pyproject.toml)
```

### Настройка переменных окружения
Создайте `.env` в корне проекта, скопируйте в файл содержимое `.env.example`. Получите API-ключ на [OpenRouter](https://openrouter.ai/). Укажите в `OPENROUTER_API_KEY` ваш ключ без кавычек.


### Запуск приложения
```
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
После запуска Swagger UI будет доступен по адресу: http://localhost:8000/docs


### Проверка кода линтером 
```
uv run ruff check
```

# API эндпоинты 

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/auth/register` | Регистрация нового пользователя |
| POST | `/auth/login` | Логин и получение JWT токена |
| GET | `/auth/me` | Получение профиля текущего пользователя |
| POST | `/chat` | Отправка сообщения LLM |
| GET | `/chat/history` | Получение истории диалога |
| DELETE | `/chat/history` | Очистка истории диалога |
| GET | `/health` | Проверка работоспособности |

# Демонстрация работы 
### 1. Регистрация пользователя

Эндпоинт POST /auth/register 

<img width="1401" height="768" alt="Снимок экрана 2026-03-22 в 00 01 22" src="https://github.com/user-attachments/assets/28817abe-31d7-4522-9de2-ac94018ebe21" />

<img width="1390" height="649" alt="Снимок экрана 2026-03-22 в 00 01 42" src="https://github.com/user-attachments/assets/14c413ae-39a5-460f-a1ae-1e1ccb9828ac" />

### 2. Логин и получение JWT токена

Эндпоинт POST /auth/login 

<img width="1279" height="808" alt="Снимок экрана 2026-03-22 в 00 09 04" src="https://github.com/user-attachments/assets/402e5102-2107-447e-b6e5-6fd9a6680cdc" />

<img width="1298" height="537" alt="Снимок экрана 2026-03-22 в 00 10 13" src="https://github.com/user-attachments/assets/d7258927-f574-4489-9194-a5f7dfc99f57" />

### 3. Авторизация в Swagger

<img width="588" height="532" alt="Снимок экрана 2026-03-22 в 00 11 34" src="https://github.com/user-attachments/assets/6444ff9e-6c5e-4fd3-bde3-0837f9b5c3a4" />

<img width="585" height="418" alt="Снимок экрана 2026-03-22 в 00 11 54" src="https://github.com/user-attachments/assets/330fef2d-301f-46cb-aa40-52551145d579" />


### 4. Профиль пользователя

Эндпоинт GET /auth/me

<img width="1342" height="776" alt="Снимок экрана 2026-03-22 в 00 13 49" src="https://github.com/user-attachments/assets/cc916895-4d32-49b5-af42-3cbe88d98de0" />

### 5. Отправка запроса к LLM

Эндпоинт POST /chat 

<img width="1284" height="691" alt="Снимок экрана 2026-03-22 в 00 17 52" src="https://github.com/user-attachments/assets/71376daf-e7b4-4306-8cb8-018cb62a8a05" />

<img width="1282" height="605" alt="Снимок экрана 2026-03-22 в 00 18 30" src="https://github.com/user-attachments/assets/14a7c191-1d9a-4da5-90d5-56f57e2dd2b2" />

### 6. Получение истории 

Эндпоинт GET /chat/history 

<img width="1282" height="278" alt="Снимок экрана 2026-03-22 в 00 21 16" src="https://github.com/user-attachments/assets/c6153bc5-4a80-48f0-a668-85e929632f39" />

<img width="1291" height="771" alt="Снимок экрана 2026-03-22 в 00 21 57" src="https://github.com/user-attachments/assets/93ef2cdc-a07f-47f0-a0ec-0248aed7b3af" />

### 7. Удаление истории 

Эндпоинт DELETE /chat/history 

<img width="1303" height="799" alt="Снимок экрана 2026-03-22 в 00 22 58" src="https://github.com/user-attachments/assets/c074ff0e-ce75-4478-b52d-f15795f6c40d" />

Повторный GET для проверки корректности работы 

<img width="1293" height="758" alt="Снимок экрана 2026-03-22 в 00 23 17" src="https://github.com/user-attachments/assets/b9c786fc-c3e8-448a-a65e-fb34b360a5db" />

### 8. Проверка работоспособности

Эндпоинт GET /health

<img width="966" height="758" alt="Снимок экрана 2026-03-22 в 00 24 12" src="https://github.com/user-attachments/assets/a7355734-5c16-4aee-97bf-49d9bac55e6c" />
