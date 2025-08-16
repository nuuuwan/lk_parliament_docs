FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive MOZ_HEADLESS=1

# Firefox + required system libs for headless
RUN apt-get update && apt-get install -y --no-install-recommends \
      firefox-esr \
      curl ca-certificates \
      # Headless runtime libs
      libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 \
      libxi6 libxrandr2 libxrender1 libxt6 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
      libatspi2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libgbm1 fonts-liberation \
      ghostscript git libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Geckodriver 0.36.0 (multi-arch)
ARG GECKODRIVER_VERSION=0.36.0
ARG TARGETARCH
RUN set -eux; \
    rm -f /usr/bin/geckodriver /usr/local/bin/geckodriver || true; \
    case "$TARGETARCH" in \
      amd64)  GD_ARCH=linux64 ;; \
      arm64)  GD_ARCH=linux-aarch64 ;; \
      *) echo "Unsupported TARGETARCH: $TARGETARCH" >&2; exit 1 ;; \
    esac; \
    curl -fsSL -o /tmp/geckodriver.tgz \
      "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-${GD_ARCH}.tar.gz"; \
    tar -xzf /tmp/geckodriver.tgz -C /usr/local/bin geckodriver; \
    rm /tmp/geckodriver.tgz; \
    chmod +x /usr/local/bin/geckodriver; \
    geckodriver --version; \
    firefox-esr --version || true

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app