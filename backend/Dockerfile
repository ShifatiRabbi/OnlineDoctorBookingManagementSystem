FROM python:3.13.7

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# useful tools for waiting on services
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl netcat-traditional \
 && rm -rf /var/lib/apt/lists/*

# install deps first for better caching
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY backend /app

# entrypoint that waits for DB, runs migrations, then starts server
COPY docker/backend.entrypoint.sh /entrypoint.sh
# fix CRLF on Windows & make executable
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
