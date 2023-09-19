FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
