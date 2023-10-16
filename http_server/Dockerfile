FROM python:alpine

RUN pip install flask psycopg2-binary

WORKDIR /usr/app/src

COPY ./ ./

CMD ["python3", "app.py"]