# Use an official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip first
RUN python -m pip install --upgrade pip

# Create a virtual environment
RUN python -m venv /opt/venv

# Install dependencies inside the venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set PATH to include venv binaries
ENV PATH="/opt/venv/bin:$PATH"

# Expose port if needed (optional)
# EXPOSE 8080

# Command to run your bot
CMD ["python", "main.py"]
