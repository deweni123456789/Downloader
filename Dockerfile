FROM python:3.12-slim

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Create venv
RUN python -m venv /opt/venv

# Install Python dependencies inside venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "main.py"]
