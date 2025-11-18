# 🚀 Швидкий старт

## 1. Встановлення та запуск

```bash
# Перейти в директорію проєкту
cd /home/pirog/Projects/College/HT/LR07-09

# Активувати віртуальне середовище (якщо не активоване)
source venv/bin/activate

# Запустити сервер
uvicorn src.main:app --reload --port 8080
```

Відкрийте: http://localhost:8080/docs

## 2. Тестування ендпоінтів

```bash
# Головна сторінка
curl http://localhost:8080/

# Health check
curl http://localhost:8080/health

# Пілоти (сирі дані)
curl http://localhost:8080/external/data/drivers

# Пілоти (оброблені)
curl http://localhost:8080/external/processed/drivers

# Турнірна таблиця
curl http://localhost:8080/external/processed/standings

# HTML сторінка
open http://localhost:8080/external/f1/html
```

## 3. Підготовка до деплою на Railway

```bash
# Ініціалізувати git (якщо ще не зроблено)
git init

# Додати всі файли
git add .

# Закомітити
git commit -m "Initial commit: F1 API FastAPI application"

# Створити репозиторій на GitHub
# Перейти на: https://github.com/new

# Підключити GitHub
git remote add origin https://github.com/YOUR_USERNAME/f1-api-fastapi.git
git branch -M main
git push -u origin main
```

## 4. Деплой на Railway

1. Зареєструйтесь: https://railway.app/
2. Login через GitHub
3. New Project → Deploy from GitHub repo
4. Виберіть репозиторій `f1-api-fastapi`
5. Railway автоматично задеплоїть
6. Settings → Generate Domain

## 5. Скріншоти для звіту

Зробіть скріншоти:
- ✅ Swagger UI (`/docs`)
- ✅ GET `/external/data/drivers`
- ✅ GET `/external/processed/drivers`
- ✅ GET `/external/data/standings`
- ✅ GET `/external/processed/standings`
- ✅ GET `/external/f1/html`
- ✅ Railway dashboard
- ✅ GitHub репозиторій

## Змінні середовища (.env)

Файл `.env` вже створений з налаштуваннями:
- PORT=8080
- ERGAST_API_BASE_URL=http://ergast.com/api/f1
- Інші налаштування

## Структура проєкту

```
LR07-09/
├── src/
│   ├── main.py                   # Головний файл
│   └── external_api/
│       ├── config.py             # Конфігурація
│       ├── models.py             # DTO моделі
│       ├── service.py            # Сервіси
│       └── router.py             # Роутери
├── venv/                         # Віртуальне середовище ✅
├── .env                          # Змінні середовища ✅
├── Dockerfile
├── requirements.txt
└── README.md
```

---

**Готово! Проєкт налаштований і готовий до використання! 🏎️**
