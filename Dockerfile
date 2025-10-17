FROM python:3.12.0-slim

WORKDIR /app

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements without torch/torchvision
COPY requirements.txt .

# Upgrade pip first
RUN python -m pip install --upgrade pip

# Install torch separately with PyTorch index
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set env
ENV PYTHONUNBUFFERED=1

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
