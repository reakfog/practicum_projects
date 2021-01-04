# Yatube
Сайт с системой публикации блогов пользователей.

## Содержание
1. [Описание проекта](#description)
2. [Стэк технологий](#stack)
3. [Технические требования](#requirements)
4. [Запуск проекта локально](#lounch)
5. [Полезные ссылки](#links)

## <a name='description'>Описание проекта</a>
**№** | **Элементы сайта** | **Пользовательский функционал** | **Возможности администраторов** *
:--- | :--- | :--- | :---
1 | Вход | Пользовательская форма |
2 | Выход | | Возможность завершить сеанса пользователя
3 | Регистрация | Пользовательская форма |
4 | Изменение пароля | Пользовательская форма |
5 | Посты | Создание (пользовательская форма), редактирование, комментирование, указание группы, добавление картинок | Удаление
6 | Страницы пользователей | Подписка, просмотр всех постов пользователя
7 | Группы | Просмотр | Создание, удаление
8 | Глобальная лента новостей | Просмотр всех постов |
9 | Личная лента новостей | Просмотр постов интересных пользователю авторов |
10 | Flatpages | Просмотр | Создание, удаление

> Возможности администраторов полностью дублируют пользовательский функционал и включают в себя дополнительные функции.

## <a name='stack'>Стек технологий</a>
Python3, Django 2.2, SQLite

## <a name='requirements'>Технические требования</a>
Все необходимые пакеты перечислены в requirements.txt

## <a name='lounch'>Запуск проекта локально</a>
Необходимо чтобы на локальном компьютере был установлен Python3 и были выполнены следующие условия:
1. Склонируйте репозиторий на локальный компьютер
2. В корневой директории проекта установите виртуальное окружение

   `python3 -m venv venv`
3. В директории ./yatube создайте файл .env и пропишите в нем SECRET_KEY - секретный ключ Django проекта
4. Установите необходимые библиотеки:

   `pip install -r requirements.txt`
5. Примените все необходимые миграции:

   `python manage.py makemigrations`

   `python manage.py migrate`
6. Для доступа к панели администратора создайте администратора:

   `python manage.py createsuperuser`
7. Запустите локальный сервер:

   `python manage.py runserver`

> Приложение будет доступно в браузере по адресу http://127.0.0.1:8000/.

## <a name='links'>Полезные ссылки</a>
+ [Django documentation](https://docs.djangoproject.com/en/3.1/)
+ [Django Girls](https://tutorial.djangogirls.org/ru/)
+ [Django book](https://djbook.ru/rel3.0/genindex.html)
+ [Эффективный Django. Часть 1](https://habr.com/ru/post/240463/)
+ [Эффективный Django. Часть 2](https://habr.com/ru/post/242261/)
+ [Ngrok](https://dashboard.ngrok.com/get-started/setup)
+ [Создание сайта на Джанго за час](https://www.youtube.com/watch?v=6K83dgjkQNw)
