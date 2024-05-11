FROM python:3.11

RUN mkdir app
COPY requirements.txt app/

RUN cd app && pip install -r requirements.txt

COPY main.py app/
EXPOSE 8000
CMD cd app && ls && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000