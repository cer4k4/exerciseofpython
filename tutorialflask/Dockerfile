#FROM python:3.8-slim-buster
FROM python:3.10-bullseye
# ENV TZ="Asia/Tehran"

EXPOSE 8000

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app
# RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt



CMD ["python3", "./main.py"]
