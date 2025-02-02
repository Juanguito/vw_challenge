FROM python:3.11

WORKDIR /app

COPY requirements/prod/requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
