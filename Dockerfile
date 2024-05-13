FROM python:3.11-bookworm

RUN mkdir app
COPY requirements.txt app/
RUN apt update && apt-get -y install netcat-traditional
RUN cd app && pip install -r requirements.txt

COPY src app/
COPY .env app/
EXPOSE 8000
CMD cd app && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000