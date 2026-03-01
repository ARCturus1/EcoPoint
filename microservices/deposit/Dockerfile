FROM python:3.14.3

COPY /common /app/common

COPY /microservices/deposit /app/microservices/deposit

WORKDIR /app/microservices/deposit

RUN pip install -r requirements.txt

CMD ["python", "main.py"]