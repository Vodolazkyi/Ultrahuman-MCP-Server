# Налаштування Ultrahuman API

Детальні інструкції з отримання доступу до Ultrahuman API та налаштування MCP сервера.

## 📋 Необхідні дані

Для роботи з Ultrahuman API вам потрібно:

1. **Authorization Key (API Token)** - 40-символьний ключ для доступу до API
2. **Data Sharing Code** - код для отримання дозволу користувачів  
3. **User Email** - email користувача Ultrahuman для тестування

## 🔑 Як отримати API Token (Authorization Key)

### Крок 1: Зв'язатися з підтримкою Ultrahuman
API доступ надається на запит. Щоб отримати токен:

1. **Напишіть в підтримку Ultrahuman:**
   - 📧 Email: [support@ultrahuman.com](mailto:support@ultrahuman.com)
   - 🌐 Сайт: [ultrahuman.com](https://ultrahuman.com)
   - 💬 Чат в додатку Ultrahuman

2. **Вкажіть у запиті:**
   - Мета використання (наприклад, "розробка MCP інтеграції для AI асистентів")
   - Ваш проект/додаток
   - Технічні деталі інтеграції

### Крок 2: Отримання доступу
Зазвичай команда Ultrahuman відповідає протягом 1-3 робочих днів та надає:
- **API Documentation** - технічну документацію
- **Authorization Key** - токен доступу
- **Data Sharing Code** - код для користувачів

### Крок 3: Активація доступу

Ви отримаєте доступи у форматі:
```
Authorization Key: abcd1234567890efgh...xyz (40 символів)
Data Sharing Code: ABC123 (6-значний код)
API Environment: Production або Staging
```

## 🔧 Налаштування змінних середовища

### Для локальної розробки:

1. Скопіюйте файл `env.example` в `.env`:
```bash
cp env.example .env
```

2. Відредагуйте `.env` файл:
```bash
# Ultrahuman API Configuration
ULTRAHUMAN_AUTH_KEY=your_real_40_character_key_here
ULTRAHUMAN_BASE_URL=https://partner.ultrahuman.com/api/v1
ULTRAHUMAN_DEFAULT_EMAIL=your_ultrahuman_email@example.com

# Server Configuration  
PORT=8000
```

### Для Railway деплойменту:

1. Відкрийте Railway dashboard
2. Перейдіть в ваш Railway проект
3. Відкрийте вкладку "Variables"
4. Додайте змінні:

```
ULTRAHUMAN_AUTH_KEY = your_real_40_character_key_here
ULTRAHUMAN_BASE_URL = https://partner.ultrahuman.com/api/v1  
ULTRAHUMAN_DEFAULT_EMAIL = your_ultrahuman_email@example.com
```

## 👤 Налаштування користувача для тестування

### Крок 1: Data Sharing Code
Користувач повинен ввести ваш **Data Sharing Code** в Ultrahuman app:

1. Відкрити Ultrahuman app
2. Перейти в Settings → Data Sharing  
3. Ввести ваш 6-значний код
4. Підтвердити надання доступу

### Крок 2: Отримання email
Після надання доступу використовуйте email користувача для API запитів.

## 🧪 Тестування API

### Використання curl:
```bash
curl --location --request GET \
'https://partner.ultrahuman.com/api/v1/metrics?email=user@example.com&date=2024-01-15' \
--header 'Authorization: your_40_character_key_here'
```

### Використання MCP сервера:
```python
# Через MCP tools
result = await get_user_metrics("user@example.com", "2024-01-15")

# Або через default user
result = await get_default_user_metrics("2024-01-15")
```

## 🌍 API Environments

### Production (Live):
```
Base URL: https://partner.ultrahuman.com/api/v1
Description: Реальні дані користувачів
```

### Staging (Test):
```
Base URL: https://staging.ultrahuman.com/api/v1
Description: Тестові дані для розробки
```

## 📊 Доступні метрики

Через API ви отримаєте доступ до:

### Основні метрики:
- **Sleep Data** - тривалість, якість, фази сну
- **Movement Data** - активність, кроки, калорії
- **Heart Rate** - ЧСС, зони навантаження
- **HRV** - варіабельність серцевого ритму
- **Temperature** - температура тіла
- **Steps** - щоденна кількість кроків

### Метаболічні метрики:
- **Glucose** - рівень глюкози (з CGM)
- **Glucose Variability** - стабільність цукру (%)
- **Average Glucose** - середній рівень (mg/dL)
- **HbA1c** - довгостроковий контроль глюкози
- **Time in Target** - час в цільовому діапазоні (%)
- **Metabolic Score** - загальна метаболічна оцінка

### Фітнес метрики:
- **Recovery Index** - індекс відновлення
- **Movement Index** - якість рухової активності  
- **VO2 Max** - аеробна витривалість

## 🔐 Безпека

### Важливо:
- ❌ **Ніколи не публікуйте** Authorization Key в публічному коді
- ✅ **Завжди використовуйте** змінні середовища
- 🔒 **Зберігайте** ключі в захищених сховищах
- 🔄 **Регулярно ротуйте** API ключі

### Приклад НЕправильного використання:
```python
# ❌ НЕ РОБІТЬ ТАК!
ULTRAHUMAN_AUTH_KEY = "abcd1234567890..." # Hard-coded key
```

### Приклад правильного використання:
```python
# ✅ ПРАВИЛЬНО
ULTRAHUMAN_AUTH_KEY = os.getenv("ULTRAHUMAN_AUTH_KEY")
```

## 🆘 Підтримка

### При проблемах з API:
- 📧 **Ultrahuman Support**: [support@ultrahuman.com](mailto:support@ultrahuman.com)
- 📚 **API Documentation**: Надається після отримання доступу
- 🔧 **Technical Issues**: Через email підтримки
- 💬 **App Support**: В додатку Ultrahuman → Settings → Support

### При проблемах з MCP сервером:
- 🐛 **GitHub Issues**: [Ultrahuman-Server Issues](https://github.com/Vodolazkyi/Ultrahuman-Server/issues)
- 📖 **FastMCP Docs**: [gofastmcp.com](https://gofastmcp.com)

## ✅ Checklist налаштування

- [ ] Написав в підтримку Ultrahuman для отримання API доступу
- [ ] Отримав Authorization Key (40 символів)
- [ ] Отримав Data Sharing Code (6 цифр)
- [ ] Налаштував змінні середовища
- [ ] Користувач ввів Data Sharing Code в додатку
- [ ] Протестував API запит з curl
- [ ] Запустив MCP сервер локально
- [ ] Задеплоїв на Railway з правильними змінними
- [ ] Протестував MCP tools через ChatGPT/Claude

**Готово! 🚀 Ваш Ultrahuman MCP сервер готовий до роботи.**
