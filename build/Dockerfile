FROM python:3.11-slim

WORKDIR /app

COPY .. .

RUN pip3 install --no-cache-dir -r requirements.txt

# CMD ["fastapi", "run", "src/app.py", "--host", "0.0.0.0", "--port", "8000"]