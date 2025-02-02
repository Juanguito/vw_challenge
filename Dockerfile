FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements/prod/requirements.txt

COPY . .

EXPOSE 8000
