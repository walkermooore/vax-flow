FROM python:3.13

#FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
#FROM ghcr.io/astral-sh/uv:latest

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libmagic1 libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . /app

WORKDIR /app
# uv 
RUN uv sync --frozen --no-cache
#RUN uv sync --frozen no-cache
# Expose port
EXPOSE 8000

# Run the application
CMD /app/.venv/bin/alembic upgrade head && /app/.venv/bin/fastapi run app/main.py --port 8000 --host 0.0.0.0