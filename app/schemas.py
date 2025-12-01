from pydantic import BaseModel
from typing import Optional, List

class VQARequest(BaseModel):
    question: str

class VQAResponse(BaseModel):
    answer: str
    confidence: Optional[float] = None
    model: str

class CaptionRequest(BaseModel):
    pass

class CaptionResponse(BaseModel):
    caption: str
    model: str

class OCRResponse(BaseModel):
    text: str
    model: str

class ObjectDetectionResponse(BaseModel):
    detections: List[dict]
    model: str

class TextToImageRequest(BaseModel):
    prompt: str

class TextToImageResponse(BaseModel):
    image: str  # base64 encoded image
    model: str

class ErrorResponse(BaseModel):
    detail: str
    error_code: str

class SystemStatus(BaseModel):
    device: str
    device_type: str
    models_loaded: bool
    active_models: List[str]
    cuda_available: bool = False
    mps_available: bool = False