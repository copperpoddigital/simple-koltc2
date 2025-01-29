# Base image with minimal footprint
FROM python:3.6-slim

# Container metadata
LABEL maintainer="Simple To-Do List Team" \
      version="1.0" \
      description="Simple To-Do List CLI Application" \
      vendor="Todo App Organization"

# Environment configuration
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    APP_USER=todoapp \
    APP_GROUP=todoapp

# Create non-root user and set up directory structure
RUN groupadd -r $APP_GROUP && \
    useradd -r -g $APP_GROUP $APP_USER && \
    mkdir -p /app /app/data && \
    chown -R $APP_USER:$APP_GROUP /app

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY src/cli/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

# Copy application code
COPY src/cli/ .

# Set secure permissions
RUN chmod -R 755 /app && \
    chmod -R 600 /app/data && \
    chown -R $APP_USER:$APP_GROUP /app

# Switch to non-root user
USER $APP_USER

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c 'import main; print("healthy")'

# Application entrypoint
CMD ["python", "main.py"]