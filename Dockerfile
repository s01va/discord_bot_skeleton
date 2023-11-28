FROM python:3.11

LABEL authors="s01va"
MAINTAINER jinn0525@gmail.com

COPY . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt

CMD ["python", "main.py"]