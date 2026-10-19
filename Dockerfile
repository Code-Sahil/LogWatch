
FROM python:3.12-slim

WORKDIR /app

COPY main.py .

RUN mkdir -p /app/logs /app/reports


ENTRYPOINT ["python", "main.py"]
CMD []

