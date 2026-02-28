# Используем официальный образ KrakenD
FROM krakend

# Метаданные
LABEL description="KrakenD API Gateway for Microservices"

# Копируем конфигурацию в образ
# (Это надежнее, чем монтировать volume в продакшене)
COPY krakend.json /etc/krakend/krakend.json

# Создаем директорию для конфигурации
WORKDIR /etc/krakend

# Копируем скрипт проверки конфигурации при старте
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Открываем порт
EXPOSE 8080

# Используем entrypoint для валидации перед запуском
# ENTRYPOINT ["/entrypoint.sh"]
CMD ["run", "-c", "/etc/krakend/krakend.json", "-p", "8080"]