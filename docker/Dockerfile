FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive MOZ_HEADLESS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      firefox-esr \
      curl ca-certificates \
      ghostscript git \
      libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app