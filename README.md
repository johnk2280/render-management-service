# render-management-service

Реализация прототипа рендер фермы. Прототип представляет из себя клиент-серверное приложение предназначенное для отслеживания статуса своих задач на рендер ферме.
 
1. Клиент.  Консольное приложение со следующими возможностями:

    ◦ регистрация пользователя

    ◦ создание новой задачи

    ◦ отображение списка созданных задач (id, status)

    ◦ отображение истории смены статусов задачи

2. Сервер. Принимает от клиента запросы и обрабатывает их.

    ◦ Регистрация пользователя с занесением его в базу данных.

    ◦ Создание новой задачи для конкретного пользователя с занесением ее в базу данных.

    ◦ Обработка запроса списка текущих задач.

**Стек: Python 3.8, Django REST Framework, PostgreSQL, Celery, Redis.**

### Инструкция по установке локально.

1. Склонируйте репозиторий на локальную машину.
2. Настройте виртуальное окружение и обновите pip.
3. Установите зависимости командой:

          $ pip3 install -r requirements.txt
          
                   
5. Создайте базу данных:


           $ sudo -u postgres psq

           postgres=# CREATE DATABASE <db_name> OWNER <owner_name>;


6. В директории основного приложения создайте файл **.env** и заполните на основе шаблона **.env.template**
7. Перейдите в директорию проекта и выполните миграции командой:
            
           $ python manage.py migrate
           
8. Если миграций не случилось и вылетело исключение, необходимо удалить файлы миграций и создайте и выполните миграции заново:

           $ python manage.py makemigrations

           $ python manage.py migrate

10. Запустите проект:

           $ python manage.py runserver
           

### Запуск клиентского приложения и работа с API.

11. Прежде чем запустить клиентское приложение, необходимо запустить Redis в docker-контейнере командой:


            $ docker run -d -p 6379:6379 redis
            
12. После того, как контейнер с Redis запустится, необходимо запустить Celery командой:

            $ celery -A renderservice worker --loglevel=INFO
            
            
13. Далее можно переходить к работе с клиентским приложением. 
Клиентское приложение является приложением с интерфейсом командной строки (CLI). Запускающий файл приложения **clien_app.py** находится в директории **client**.


