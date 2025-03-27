# Use a lightweight Python base image
FROM python:3.9-alpine3.18 AS base

LABEL maintainer="srishtinonstopio"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# Install system dependencies
RUN apk add --no-cache \
    bash \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    && python -m venv /py

# Upgrade pip and install dependencies in a separate layer
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN /py/bin/pip install --no-cache-dir --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Set up development dependencies only when ARG DEV=true
ARG DEV=false
RUN if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi

# Remove temporary files
RUN rm -rf /tmp

# Create a non-root user for security
RUN adduser --disabled-password --no-create-home django-user

# Copy application files
COPY ./app /app
WORKDIR /app

# Set permissions
RUN chown -R django-user:django-user /app

# Expose port
EXPOSE 8000

# Switch to non-root user
USER django-user

# Default command (can be overridden in Docker Compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
