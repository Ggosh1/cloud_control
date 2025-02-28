FROM python:3.9-slim
WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install flask flask_sqlalchemy validators

EXPOSE 5000

CMD ["python", "main.py"]
