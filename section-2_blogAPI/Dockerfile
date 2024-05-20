FROM python:3.10.12-slim

WORKDIR /blogAPI

copy requirements.txt .

RUN pip install -r requirements.txt

copy . .

EXPOSE 8000
