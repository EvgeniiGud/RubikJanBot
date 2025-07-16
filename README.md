## RubikJanBot
Description for RubikJanBota

### Все зависимости находяться в файле requirements.txt
> Что бы автоматически установить все зависмости надо в терминале использовать команду
- pip install -r dev_requirements.txt  # на локальном для разработки
- pip install -r prod_requirements.txt  # на основном сервере

### Безопасное использование конфигурационных переменых в проекте (например BOT_TOKEN)
from config import BOT_TOKEN

#### Работа с alembic
- alembic revision --autogenerate -m "Added users table" # Данная команда создает правила миграции 
- alembic upgrade head # применение миграции


### Используемые библиотеки для работы бота
#### base_requirements
- python-dotenv           # для безопасного использования пременных в проекте
- pyTelegramBotAPI        # фреймвок для создания асинхронного tg бота
- aiohttp
- SQLAlchemy==2.0.41      # для создания таблиц в БД
- alembic==1.16.2         # для миграции таблиц в базу данных
   
#### prod_requirements
- psycopg-binary==2.9.10  # для работы с постгри
- aiopg==1.4.0            # асинхронная работа с постгри

#### dev_requirements
- aiosqlite==0.21.0       # асинхронный клиент для баз данных sqlite на локальной машине