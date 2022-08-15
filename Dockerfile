FROM python:3.10.4

COPY renderservice /renderservice
WORKDIR /renderservice
COPY requirements.txt .

EXPOSE 8080

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations && python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

