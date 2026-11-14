FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/user \
    MPLCONFIGDIR=/tmp/matplotlib \
    PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ffmpeg espeak-ng libespeak1 libportaudio2 \
    libgl1 libglib2.0-0 libgomp1 poppler-utils libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt \
    && python -m pip check
RUN useradd --create-home --uid 1000 user
COPY --chown=user:user . /app
USER user

EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
    CMD curl --fail --silent http://127.0.0.1:7860/api/health || exit 1

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860", "--no-server-header"]
