# Use a lightweight Python image with glibc support
FROM python:3.9-slim AS test

# Maintainer information
LABEL maintainer="srishtinonstopio"

# Ensure output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install necessary dependencies for psycopg2 and other build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy application code
COPY ./app /app

# Expose port 8000 for Django
EXPOSE 8000

# Argument to specify development mode
ARG DEV=false

# Install dependencies and set up a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    useradd --no-create-home django-user

# Set the correct path for virtual environment
ENV PATH="/py/bin:$PATH"

# Run container as django-user instead of root
USER django-user
