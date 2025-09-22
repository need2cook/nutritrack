FROM python:3.11-slim

# рабочая директория
WORKDIR /app

# зависимости для asyncpg и psycopg2
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ставим питон-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем проект
COPY . .

# запускаем через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
