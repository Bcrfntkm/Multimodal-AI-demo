import torch
from app.core.config import settings

def get_device():
    if settings.DEVICE == "cuda" and torch.cuda.is_available():
        return torch.device("cuda")
    elif settings.DEVICE == "mps" and torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")
    
def get_device_info():
    device = get_device()
    info = {
        "device": str(device),
        "device_type": settings.DEVICE,
        "cuda_available": torch.cuda.is_available(),
        "mps_available": torch.backends.mps.is_available(),
    }

    if device.type == "cuda":
        info.update({
            "cuda_device": torch.cuda.current_device(),
            "cuda_device_name": torch.cuda.get_device_name(),
            "cuda_memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
        })
    elif device.type == "mps":
        info.update({
            "mps_device": "MPS",
        })

    return info

def optimize_for_device(model, device):
    model = model.to(device)

    if device.type == "cpu":
        model = model.to(torch.float32)
    elif device.type == "cuda":
        # Check if the model supports half precision
        try:
            model = model.to(torch.float16 if torch.cuda.is_bf16_supported() else torch.float32)
        except:
            # Some models may not support float16, keep as float32
            model = model.to(torch.float32)
            
        if torch.cuda.device_count() > 1:
            model = torch.nn.DataParallel(model)
    elif device.type == "mps":
        # MPS support - use float32 as MPS has limited float16 support
        model = model.to(torch.float32)

    return model