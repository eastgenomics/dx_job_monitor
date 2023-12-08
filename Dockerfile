# syntax=docker/dockerfile:1

FROM python:3.8-slim

RUN apt-get update -y && apt-get install -y gcc

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY dx_job_monitor.py helper.py /

CMD [ "python", "dx_job_monitor.py"]