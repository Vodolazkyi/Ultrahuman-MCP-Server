# Деплоймент на Railway - Інструкції

## Статус проекту ✅

✅ **Код готовий**: Ultrahuman MCP Server повністю реалізований
✅ **Git репозиторій**: Код запушений в https://github.com/Vodolazkyi/Ultrahuman-Server
✅ **Docker конфігурація**: Dockerfile та railway.toml налаштовані
✅ **Залежності**: requirements.txt з усіма необхідними пакетами
✅ **Тестування**: Сервер успішно запускається локально

## Наступні кроки для деплойменту

### 1. Підключення до Railway

1. Відкрийте [Railway](https://railway.app)
2. Створіть новий проект з бажаною назвою
3. Виберіть "Deploy from GitHub repo"
4. Підключіть репозиторій: `https://github.com/Vodolazkyi/Ultrahuman-Server`

### 2. Налаштування змінних середовища

В Railway Dashboard встановіть наступні змінні:

```bash
ULTRAHUMAN_AUTH_KEY=your_40_character_authorization_key_here
ULTRAHUMAN_BASE_URL=https://partner.ultrahuman.com/api/v1
ULTRAHUMAN_DEFAULT_EMAIL=your_ultrahuman_email@example.com
PORT=8000
```

**Важливо**: 
- `ULTRAHUMAN_AUTH_KEY` - ваш справжній 40-символьний ключ API від Ultrahuman
- `ULTRAHUMAN_DEFAULT_EMAIL` - email користувача для тестування (опціонально)

**📋 Як отримати API ключ**: 
- Напишіть на support@ultrahuman.com з описом вашого проекту
- Детальні інструкції: [API_SETUP.md](./API_SETUP.md)

### 3. Автоматичний деплоймент

Railway автоматично:
- Виявить Dockerfile
- Побудує контейнер
- Задеплоїть додаток
- Надасть публічний URL

### 4. Перевірка деплойменту

Після деплойменту ваш MCP сервер буде доступний за адресою:
```
https://your-project-name.railway.app/mcp
```

## Структура проекту

```
Ultrahuman-MCP-main/
├── main.py                 # Основний MCP сервер
├── requirements.txt        # Python залежності  
├── Dockerfile             # Docker конфігурація
├── railway.toml           # Railway налаштування
├── README.md              # Документація
├── examples.py            # Приклади використання
├── test_server.py         # Тестовий скрипт
├── deploy.sh              # Скрипт деплойменту
├── env.example            # Приклад змінних середовища
└── .github/workflows/     # GitHub Actions CI/CD
```

## Доступні інструменти MCP

1. **get_default_user_metrics** - Отримати всі метрики для default користувача (з env)
2. **get_user_metrics** - Отримати всі метрики здоров'я конкретного користувача
3. **get_sleep_data** - Дані про сон
4. **get_movement_data** - Дані про рух та активність  
5. **get_glucose_metrics** - Метрики глюкози
6. **get_heart_metrics** - Серцеві метрики (ЧСС, HRV, VO2 Max)

## Доступні метрики

- Sleep Data (дані сну)
- Movement Data (дані руху)
- Heart Rate (частота серця)
- HRV (варіабельність серцевого ритму)
- Temperature (температура)
- Steps (кроки)
- Glucose (глюкоза)
- Metabolic Score (метаболічний рахунок)
- Glucose Variability (варіабельність глюкози)
- Average Glucose (середня глюкоза)
- HbA1c
- Time in Target (час в цільовому діапазоні)
- Recovery Index (індекс відновлення)
- Movement Index (індекс руху)
- VO2 Max

## Використання API

### Приклад HTTP запиту

```bash
curl -X POST https://your-project-name.railway.app/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_user_metrics",
    "arguments": {
      "email": "user@example.com",
      "date": "2024-01-15"
    }
  }'
```

### Приклад відповіді

```json
{
  "success": true,
  "email": "user@example.com",
  "date": "2024-01-15",
  "metrics": {
    "sleep_data": {...},
    "movement_data": {...},
    "heart_rate": {...},
    "glucose": {...}
  }
}
```

## Безпека

- ✅ API ключі зберігаються в змінних середовища
- ✅ Всі запити використовують HTTPS
- ✅ Валідація даних та обробка помилок
- ✅ Немає логування чутливих даних

## Підтримка

- **Документація**: [README.md](./README.md)
- **Приклади**: [examples.py](./examples.py)
- **Тестування**: [test_server.py](./test_server.py)
- **Ultrahuman API**: https://blog.ultrahuman.com/blog/accessing-the-ultrahuman-partnership-api/

---

**Проект готовий до деплойменту! 🚀**
