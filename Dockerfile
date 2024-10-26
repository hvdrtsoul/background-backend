FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apk update && apk add tk

RUN pip install psycopg2-binary

COPY . .

RUN chmod +x /app/script.sh

CMD ["./script.sh"]