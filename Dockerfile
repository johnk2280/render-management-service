FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

COPY backend/renderservice /renderservice
WORKDIR /renderservice
COPY requirements.txt .

COPY wait-for-psql.sh .
RUN chmod +x wait-for-psql.sh

EXPOSE 8080

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
