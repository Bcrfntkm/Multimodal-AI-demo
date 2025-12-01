FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including tesseract for OCR and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for models
RUN mkdir -p ./models

# Expose port
EXPOSE 8000

# Run the application
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
