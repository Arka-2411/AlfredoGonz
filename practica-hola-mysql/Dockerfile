FROM python:3.11-slim

WORKDIR /app

COPY ./src /app

# 👇 Instalamos Flask, PyMySQL y Cryptography
RUN pip install flask pymysql cryptography

EXPOSE 5000

CMD ["python", "app.py"]
