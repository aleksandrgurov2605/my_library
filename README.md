# My library
## Небольшой тренировочный проект, который позволяет добавлять/просматривать/редактировать/удалять данные о книгах.
# Стек технологий
- Python 3.13+
- FastAPI — веб-фреймворк.
- SQLAlchemy — ORM для работы с базой данных.
- Pydantic — валидация данных.
- Alembic — миграции базы данных.
- PostgreSQL — база данных.
- Uvicorn — ASGI-сервер.
- Pytest — тестирование.
# Установка и запуск
## Стандартный способ. С использованием пакетного менеджера pip.
1. Клонирование репозитория
```bash
git clone https://github.com/aleksandrgurov2605/my_library.git
cd my_library
git checkout docker
```

2. Настройка виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
```
 или
```bash
venv\Scripts\activate     # Для Windows
```

3. Установка зависимостей
```bash
pip install -r requirements.txt
```

4. Настройка переменных окружения
Отредактируйте следующий файл, удалив 'example' из названия и указав недостающие значения переменных:  
- example.env 
- example.docker.env, если вы собираетесь запускать приложение, используя контейнеры Docker

5. Запуск приложения  
5.1. Стандартный запуск приложения  
Создайте базу данных Postgres.  
После этого примените миграции, выполнив команду
```bash
alembic upgrade head
```
Запустите приложение
```bash
uvicorn app.main:app --reload
```
5.2. Запуск приложения в контейнерах Docker
Убедитесь, что у вас установлен Docker  
Соберите и запустите контейнеры, выполнив команду
```bash
docker compose -f docker-compose.yml up -d --build
```

После этого примените миграции, выполнив команду
```bash
docker compose exec web alembic upgrade head
```
## С использованием пакетного менеджера uv
1. Установка uv
Если у вас еще не установлен uv, установите его одной командой:
```bash
# macOS/Linux
curl -LsSf astral.sh | sh
# Windows
powershell -c "ir astral.sh | iex"
```

2. Клонирование и настройка проекта
```bash
git clone https://github.com/aleksandrgurov2605/my_library.git
cd my_library
git checkout dev
```

3. Создание окружения и установка зависимостей
```bash
uv sync
```

4. Настройка переменных окружения
Отредактируйте следующий файл, удалив 'example' из названия и указав недостающие значения переменных:
- example.env 
- example.docker.env, если вы собираетесь запускать приложение, используя контейнеры Docker

5. Запуск приложения  
5.1. Стандартный запуск приложения  
Создайте базу данных Postgres.  
После этого примените миграции, выполнив команду
```bash
uv run alembic upgrade head
```
Запустите приложение
```bash
uv run uvicorn app.main:app --reload
```
5.2. Запуск приложения в контейнерах Docker
Убедитесь, что у вас установлен Docker    
Соберите и запустите контейнеры, выполнив команду
```bash
docker compose -f docker-compose.yml up -d --build
```
После этого примените миграции, выполнив команду
```bash
docker compose exec web alembic upgrade head
```
Для остановки контейнеров Docker
```bash
docker compose stop
```
Для повторного запуска контейнеров Docker
```bash
docker compose up -d
```

### Приложение будет доступно по адресу: http://127.0.0.1:8000
# Документация API
### После запуска проекта интерактивная документация доступна по ссылкам:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
# Структура проекта
```text
.
├── app  
│   ├── core                 # Настройки проекта, конфигурация переменных окружения
│   │   └──  config.py       
│   ├── db                   # Настройка подключения к БД 
│   │   ├──  __init__.py         
│   │   ├──  database.py   
│   │   └──  db_depends.py
│   ├── migrations           # Миграции alembic
│   │   ├──  versions                
│   │   ├──  env.py                 
│   │   ├──  README                 
│   │   └──  script.py.mako  
│   ├── models               # Модели SQLAlchemy
│   │   ├──  __init__.py        
│   │   └──  books.py        
│   ├── repositories         # Репозиторий. Операции с БД.
│   │   ├──  __init__.py        
│   │   └──  books.py        
│   ├── routers              # Эндпоинты(роуты).
│   │   ├──  __init__.py        
│   │   └──  books.py        
│   ├── schemas              # Схемы Pydantic 
│   │   ├──  __init__.py        
│   │   └──  books.py        # Схемы Pydantic  
│   ├── __init__.py   
│   ├── Dockerfile           
│   ├── logger.py            # Настройки логирования
│   └── main.py              # Точка входа в приложение  
├── tests                    # Папка с тестами 
│   ├── conftest.py          # Настройка тестовой среды 
│   ├── test_api.py          # Тесты эндпойнтов  
│   └── test_mock.py         # Тесты репозитория   
├── .docker.env                
├── .env   
├── .gitignore                 
├── alembic.ini                
├── docker-compose.yml                
├── pyproject.toml           # Конфигурация проекта и зависимостей (uv)
├── README.md                # Файл-руководство.   
├── requirements.txt         # Зависимости для установки с помощью pip. 
└── uv.lock                  # Lock-файл зависимостей
 ``` 

# Тесты
Для локального запуска тестов 
```bash
pytest
```

# Лицензия
Этот проект распространяется под лицензией MIT. Подробнее в файле LICENSE.