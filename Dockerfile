FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends git gcc \
libc6-dev build-essential libcurl4-openssl-dev libssl-dev ffmpeg && \
rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt
ADD . /opt/app
WORKDIR /opt/app
ENV PYTHONPATH="${PYTHONPATH}:."
EXPOSE 8000
RUN chmod +x *.sh
CMD ["bash", "run.sh"]
