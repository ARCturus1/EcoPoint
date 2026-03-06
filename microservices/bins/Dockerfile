FROM python:3.14.3

# COPY /common /app/common

COPY . /app/microservices/bins

WORKDIR /app/microservices/bins

RUN pip install -r requirements.txt

CMD ["python", "main.py"]