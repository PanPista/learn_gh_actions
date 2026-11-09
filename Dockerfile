# Stage 1: Build dependencies
FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final minimal image
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only the installed packages without pip cache
COPY --from=builder /install /usr/local
COPY . .

# Create a non-privileged user for security
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8000"]