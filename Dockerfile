FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends curl git-core gcc \
libc6-dev build-essential libcurl4-openssl-dev libssl-dev ffmpeg && \
rm -rf /var/lib/apt/lists/*

ENV NODE_VERSION=12.6.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt
ADD . /opt/app
WORKDIR /opt/app
RUN cd /opt/app/react-components/ && npm install && npm run build-prod && cd /opt/app
ENV PYTHONPATH="${PYTHONPATH}:."
EXPOSE 8000
RUN chmod +x *.sh
CMD ["bash", "run.sh"]
