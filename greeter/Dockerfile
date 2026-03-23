FROM python:3.11-slim

WORKDIR /app

COPY greeting_api.py .

RUN pip install flask requests

ENV FLASK_APP=greeting_api.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]

