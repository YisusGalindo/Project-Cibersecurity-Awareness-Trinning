FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y ansible sqlite3
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["python", "app/app.py"]