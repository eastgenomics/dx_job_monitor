# syntax=docker/dockerfile:1

FROM python:3.8-slim-bullseye

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY dx_job_monitor.py .

CMD [ "python", "-u", "dx_job_monitor.py"]