from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.model_instance import model_captioning, model_vqa, model_ocr, model_object_detection
from app.schemas import VQARequest, VQAResponse, CaptionResponse, OCRResponse, ObjectDetectionResponse, SystemStatus
from app.core.device_utils import get_device_info
from app.core.config import settings

router = APIRouter()

@router.post("/vqa", response_model=VQAResponse)
async def visual_qa(question: str = Form(...), image: UploadFile = File(...)):
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
        
        image_data = await image.read()
        answer = model_vqa.answer(question=question, image=image_data)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing VQA: {str(e)}")
    
@router.post("/captioning", response_model=CaptionResponse)
async def image_captioning(image: UploadFile = File(...)):
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
        
        image_data = await image.read()
        answer = model_captioning.answer(image=image_data)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing captioning: {str(e)}")

@router.post("/ocr", response_model=OCRResponse)
async def ocr(image: UploadFile = File(...)):
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
        
        image_data = await image.read()
        result = model_ocr.answer(image=image_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing OCR: {str(e)}")

@router.post("/object-detection", response_model=ObjectDetectionResponse)
async def object_detection(image: UploadFile = File(...)):
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
        
        image_data = await image.read()
        result = model_object_detection.answer(image=image_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing object detection: {str(e)}")

@router.get("/system/status", response_model=SystemStatus)
async def system_status():
    device_info = get_device_info()
    return {
        "device": device_info["device"],
        "device_type": device_info["device_type"],
        "models_loaded": True,
        "active_models": [
            settings.MODEL_VQA,
            settings.MODEL_CAPTIONING,
            settings.MODEL_OCR,
            settings.MODEL_OBJECT_DETECTION
        ],
        "cuda_available": device_info.get("cuda_available", False),
        "mps_available": device_info.get("mps_available", False),
    }
