FROM python:latest

WORKDIR /app
COPY . .


RUN pip install -r requirements.txt

CMD ["flask", "--app", "app.py", "run", "-h", "0.0.0.0"]