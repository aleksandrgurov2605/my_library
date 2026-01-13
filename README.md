# My library
# Небольшой тренировочный проект, который позволяет добавлять/просматривать/редактировать/удалять данные о книгах.
# Стек технологий
## Python 3.13+
## FastAPI — веб-фреймворк.
## SQLAlchemy — ORM для работы с базой данных.
## Pydantic — валидация данных.
## SQLite — база данных.
# Установка и запуск
## Стандартный способ. С использованием пакетного менеджера pip.
1. Клонирование репозитория
```bash
git clone https://github.com/aleksandrgurov2605/my_library.git
cd my_library
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

4. Запуск приложения
```bash
uvicorn app.main:app --reload
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
```

3. Создание окружения и установка зависимостей
```bash
uv sync
```

4. Запуск приложения
```bash
uv run uvicorn app.main:app --reload
```

### Приложение будет доступно по адресу: http://127.0.0.1:8000
# Документация API
## После запуска проекта интерактивная документация доступна по ссылкам:
### Swagger UI: 127.0.0.1
### ReDoc: 127.0.0.1
# Структура проекта
```text
.
├── app  
│   ├── db                   # Настройка подключения к БД 
│   │   ├──  __init__.py     
│   │   ├──  database.py     
│   │   └──  db_depends.py   
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
│   └── main.py              # Точка входа в приложение  
├── tests                # Папка с тестами 
│   ├── conftest.py      # Настройка тестовой среды 
│   ├── test_api.py      # Тесты эндпойнтов  
│   └── test_mock.py     # Тесты репозитория   
├── .gitignore                 
├── pyproject.toml     # Конфигурация проекта и зависимостей (uv)
├── README.md          # Файл-руководство.   
├── requirements.txt   # Зависимости для установки с помощью pip. 
└── uv.lock            # Lock-файл зависимостей
 ``` 

# Лицензия
Этот проект распространяется под лицензией MIT. Подробнее в файле LICENSE.