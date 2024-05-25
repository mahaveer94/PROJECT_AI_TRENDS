FROM python:3.9-slim

WORKDIR /ai_trends_lab

COPY ai_trends_lab.py .

RUN pip install pandas numpy matplotlib

CMD ["python", "ai_trends_lab.py"]