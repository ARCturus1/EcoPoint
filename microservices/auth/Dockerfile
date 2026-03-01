FROM python:3.14.3

COPY /common /app/common

COPY /microservices/auth /app/microservices/auth

WORKDIR /app/microservices/auth

RUN pip install -r requirements.txt

CMD ["python", "main.py"]