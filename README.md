# Multimodal AI Demo

A web interface demo for multimodal models with visual question answering, image captioning, OCR, and object detection.

## Features

- **Visual Question Answering** - Ask questions about images
- **Image Captioning** - Generate descriptions for images
- **Optical Character Recognition** - Extract text from images
- **Object Detection** - Detect and locate objects in images

## Quick Start

### Docker (Recommended)

```bash
# CPU only (works on all systems)
docker-compose -f compose.cpu.yml up --build

# With GPU support (Linux with NVIDIA GPU only)
docker-compose up --build
```

### Native Execution (macOS with M-series chips)

```bash
# Create virtual environment
python3 -m venv multimodal_env
source multimodal_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with MPS support
./run_mps.sh
```

Visit `http://localhost:8000` to access the web interface.

## Configuration

The application can be configured using environment variables:

- `DEVICE` - "cuda", "mps", or "cpu" (default: "cpu")
- `PORT` - Server port (default: 8000)
- `CACHE_DIR` - Model cache directory (default: "./models")

## Model Cache Mounting

The application supports both mounting and not mounting the model cache directory:

1. **With mounting (default behavior):** The local `./models` directory is mounted to `/app/models` inside the container, persisting models between container restarts.

2. **Without mounting:** To run without mounting the models directory, simply remove or comment out the volume line in the Docker Compose files.

When the models directory is not mounted, the models will be downloaded inside the container's filesystem and will be lost when the container is removed. When the directory is mounted, the models are persisted on the host filesystem and can be reused across container restarts.

## Technical Documentation

For detailed technical information about the models used, see:
- [ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision](https://arxiv.org/abs/2102.03334)
- [BLIP: Bootstrapping Language-Image Pre-training](https://arxiv.org/abs/2201.12086)
- [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872)

## Requirements

- Docker and Docker Compose (for Docker deployment)
- Python 3.9-3.12 (for native execution)
- 8GB+ RAM recommended
- NVIDIA GPU (optional, for faster inference on Linux)

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## License

This project is licensed under the MIT License.