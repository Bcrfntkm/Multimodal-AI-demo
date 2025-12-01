from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    APP_NAME: str = "Multimodal Demo"
    DEBUG: bool = bool(os.getenv("DEBUG", False))

    DEVICE: str = os.getenv("DEVICE", "cpu")
    PORT: int = int(os.getenv("PORT", 8000))

    MODEL_VQA: str = os.getenv("MODEL_VQA", "dandelin/vilt-b32-finetuned-vqa")
    MODEL_CAPTIONING: str = os.getenv("MODEL_CAPTIONING", "Salesforce/blip-image-captioning-base")
    MODEL_OCR: str = os.getenv("MODEL_OCR", "microsoft/layoutlmv3-base")
    MODEL_OBJECT_DETECTION: str = os.getenv("MODEL_OBJECT_DETECTION", "facebook/detr-resnet-50")
    MODEL_TEXT_TO_IMAGE: str = os.getenv("MODEL_TEXT_TO_IMAGE", "runwayml/stable-diffusion-v1-5")

    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", 4))
    MAX_LENGTH: int = int(os.getenv("MAX_LENGTH", 50))

    CACHE_DIR: str = os.getenv("CACHE_DIR", "./models")

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
