### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/twotwo-d/api_yamdb.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Загрузить csv файлы в БД:

```
python manage.py importcsv
```

Запустить проект:

```
python3 manage.py runserver
```

Документация по API:

```
http://127.0.0.1:8000/redoc/
```
