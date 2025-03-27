# Use a Debian-based slim image for better compatibility
FROM python:3.9-slim AS test

LABEL maintainer="srishtinonstopio"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/py/bin:$PATH"

# Install dependencies
RUN apt-get update && apt-get install -y \
    bash \
    gcc \
    libffi-dev \
    postgresql-client \
    && python -m venv /py \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN /py/bin/pip install --no-cache-dir --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt

# Set up development dependencies only when ARG DEV=true
ARG DEV=false
RUN if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi

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

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
