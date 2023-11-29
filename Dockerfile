FROM --platform=linux/amd64 python:3.8
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/GlobalRedPyme
EXPOSE 8004
RUN python manage.py crontab add

CMD ["sh", "-c", "cron && python manage.py runserver 0.0.0.0:8004"]

