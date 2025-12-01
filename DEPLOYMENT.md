# Deployment Guide

This guide explains how to build and run the Multimodal AI Playground application.

## Table of Contents
1. [Building the Docker Image](#building-the-docker-image)
2. [Running the Application](#running-the-application)
3. [Accessing the Application](#accessing-the-application)
4. [Configuration](#configuration)
5. [GPU Configuration](#gpu-configuration)
6. [Model Management](#model-management)

## Building the Docker Image

To build the Docker image locally:

```bash
# Clone the repository
git clone <repository-url>
cd multimodal-ai-playground

# Build the Docker image
docker build -t multimodal-ai-playground .
```

## Running the Application

### CPU Mode (Recommended for macOS and general use)

```bash
# Run with CPU support
docker-compose -f compose.cpu.yml up --build
```

### GPU Mode (Linux with NVIDIA GPU only)

```bash
# Run with GPU support (requires NVIDIA Docker runtime)
docker-compose up --build
```

### Native Execution (macOS with M-series chips)

For best performance on macOS with M1/M2/M3 chips:

```bash
# Create virtual environment
python3 -m venv multimodal_env
source multimodal_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with MPS support
./run_mps.sh
```

## Accessing the Application

Once the application is running, access it through your web browser:

- **URL**: http://localhost:8000
- **Port**: 8000 (default, configurable)

## Configuration

The application can be configured using environment variables:

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DEVICE` | Processing device | `cpu` |
| `PORT` | Application port | `8000` |
| `CACHE_DIR` | Model cache directory | `./models` |
| `MODEL_VQA` | Visual Q&A model | `dandelin/vilt-b32-finetuned-vqa` |
| `MODEL_CAPTIONING` | Image captioning model | `Salesforce/blip-image-captioning-base` |
| `MODEL_OCR` | OCR model | `EasyOCR` |
| `MODEL_OBJECT_DETECTION` | Object detection model | `facebook/detr-resnet-50` |

### Changing the Port

To run the application on a different port:

**Docker:**
```bash
# Set port via environment variable
PORT=8080 docker-compose -f compose.cpu.yml up --build
```

**Native:**
```bash
# Set port via environment variable
export PORT=8080
./run_mps.sh
```

## GPU Configuration

### CPU Mode
```bash
DEVICE=cpu docker-compose -f compose.cpu.yml up --build
```

### GPU Mode (Linux with NVIDIA GPU)
```bash
DEVICE=cuda docker-compose up --build
```

### MPS Mode (macOS M-series chips)
```bash
DEVICE=mps ./run_mps.sh
```

### Requirements for GPU Support

1. **NVIDIA GPU (Linux only)**:
   - NVIDIA Driver installed
   - NVIDIA Container Toolkit installed
   - Docker Engine 19.03+

2. **macOS M-series chips**:
   - Native execution only (Docker does not support GPU passthrough on macOS)
   - Use the provided `run_mps.sh` script

## Model Management

### Model Caching

Models are automatically downloaded and cached in the `./models` directory. This directory is mounted as a Docker volume to persist models between container restarts.

### Running Without Internet Access

After initial model download, the application can run without internet access:

1. Ensure models are downloaded (run once with internet access)
2. Disconnect from the internet
3. Run the application normally

### Mounting Model Directory from Host

To use a custom model directory from the host system:

**Docker:**
```bash
# Modify the volumes section in compose.yml or compose.cpu.yml
# Replace ./models with your custom path
volumes:
  - ./app:/app/app
  - /path/to/your/models:/app/models
```

**Native:**
```bash
# Set CACHE_DIR environment variable
export CACHE_DIR=/path/to/your/models
./run_mps.sh
```

### Optional Model Directory Mounting

The application supports both mounting and not mounting the model cache directory:

1. **With mounting (default behavior):** The local `./models` directory is mounted to `/app/models` inside the container, persisting models between container restarts.

2. **Without mounting:** To run without mounting the models directory, simply remove or comment out the volume line:
   ```yaml
   volumes:
     - ./app:/app/app
     # - ./models:/app/models  # Commented out to disable mounting
   ```

When the models directory is not mounted, the models will be downloaded inside the container's filesystem and will be lost when the container is removed. When the directory is mounted, the models are persisted on the host filesystem and can be reused across container restarts.

### Model Information

The application uses the following pre-trained models:

1. **Visual Question Answering**: `dandelin/vilt-b32-finetuned-vqa`
2. **Image Captioning**: `Salesforce/blip-image-captioning-base`
3. **OCR**: `EasyOCR` with English language support
4. **Object Detection**: `facebook/detr-resnet-50`

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Use a different port
   PORT=8080 docker-compose -f compose.cpu.yml up --build
   ```

2. **Insufficient memory**:
   - Close other applications
   - Consider using CPU mode for lower memory usage

3. **Model download failures**:
   - Check internet connection
   - Ensure sufficient disk space
   - Verify model names in configuration

### Performance Tips

1. **For macOS users**: Use native execution with MPS for best performance
2. **For Linux users**: Use GPU mode if you have an NVIDIA GPU
3. **For Windows users**: Use CPU mode or WSL 2 with GPU support

## Technical Documentation

For detailed technical information about the models used, see:
- [ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision](https://arxiv.org/abs/2102.03334)
- [BLIP: Bootstrapping Language-Image Pre-training](https://arxiv.org/abs/2201.12086)
- [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872)