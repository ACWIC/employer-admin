FROM python:3.8.5-alpine

# uvicorn/uvloop need make
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev make

# Ensure terminal output is sent directly to logs
ENV PYTHONBUFFERED 1

# Install requirements
COPY ./requirements /requirements
RUN pip install -r /requirements/uvicorn.txt

WORKDIR /app

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080
