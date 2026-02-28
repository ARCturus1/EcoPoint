FROM python:3.14.3

COPY /common /app/common

COPY /microservices/user_stats /app/microservices/user_stats

WORKDIR /app/microservices/user_stats

RUN pip install -r requirements.txt

CMD ["python", "main.py"]