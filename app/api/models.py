from transformers import pipeline
from PIL import Image
from io import BytesIO
from app.core.config import settings
from app.core.device_utils import get_device, optimize_for_device
import torch
import numpy as np

class MultiModel:
    def __init__(self):
        self.device = get_device()
        self.model = None
        self.processor = None
        self.description = ""
    def load_model(self):
        pass
    def answer(self):
        pass

class VisualQA(MultiModel):
    def __init__(self):
        super(VisualQA, self).__init__()
        self.model_name = settings.MODEL_VQA
        self.description = 'visual-question-answering'
    
    def load_model(self):
        from transformers import ViltProcessor, ViltForQuestionAnswering
        print(f"Loading VQA model: {self.model_name}")
        try:
            self.processor = ViltProcessor.from_pretrained(
                self.model_name,
                cache_dir=settings.CACHE_DIR)
            
            self.model = ViltForQuestionAnswering.from_pretrained(
                self.model_name,
                cache_dir=settings.CACHE_DIR)
            self.model = optimize_for_device(self.model, self.device)
            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {str(e)}")
            raise e

    def answer(self, question, image):
        try:
            image = Image.open(BytesIO(image))
            encoding = self.processor(image, question, return_tensors="pt")
            encoding = {k: v.to(self.device) for k, v in encoding.items()}
            outputs = self.model(**encoding)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            answer = self.model.config.id2label[idx]
            return {
                'answer': answer,
                'confidence': float(torch.softmax(logits, dim=1)[0][idx].item()),
                'model': self.model_name,
            }
        except Exception as e:
            print(f"Error during VQA inference: {str(e)}")
            raise e
    
class ImageCaptioning(MultiModel):
    def __init__(self):
        super(ImageCaptioning, self).__init__()
        self.model_name = settings.MODEL_CAPTIONING
        self.description = "image_to_text"

    def load_model(self):
        print(f"Loading ImageCaptioning model {self.model_name}")
        from transformers import BlipProcessor, BlipForConditionalGeneration
        try:
            self.processor = BlipProcessor.from_pretrained(
                self.model_name,
                cache_dir=settings.CACHE_DIR,
            )
            self.model = BlipForConditionalGeneration.from_pretrained(
                self.model_name,
                cache_dir=settings.CACHE_DIR,
            )
            self.model = optimize_for_device(self.model, self.device)
        except Exception as e:
            print(f"Error loading model {self.model_name}: {str(e)}")
            raise e
    
    def answer(self, image):
        try:
            image = Image.open(BytesIO(image)).convert('RGB')
            inputs = self.processor(image, return_tensors='pt')
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            out = self.model.generate(**inputs)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            return {
                'caption': caption,
                'model' : self.model_name,
            }
        except Exception as e:
            print(f"Error during Image Captioning: {str(e)}")
            raise e

class OCRModel(MultiModel):
    def __init__(self):
        super(OCRModel, self).__init__()
        self.model_name = "EasyOCR"
        self.description = "optical-character-recognition"
        self.reader = None

    def load_model(self):
        print(f"Loading OCR model {self.model_name}")
        try:
            import easyocr
            self.reader = easyocr.Reader(['en'], gpu=(str(self.device) != "cpu"))
            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {str(e)}")
            raise e
    
    def answer(self, image):
        try:
            import numpy as np
            import cv2
            image_array = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            results = self.reader.readtext(img)
            extracted_text = " ".join([result[1] for result in results])
            if not extracted_text.strip():
                extracted_text = "No text detected in the image"
            return {
                'text': extracted_text,
                'model': self.model_name,
            }
        except Exception as e:
            print(f"Error during OCR: {str(e)}")
            raise e

class ObjectDetectionModel(MultiModel):
    def __init__(self):
        super(ObjectDetectionModel, self).__init__()
        self.model_name = settings.MODEL_OBJECT_DETECTION
        self.description = "object-detection"

    def load_model(self):
        print(f"Loading Object Detection model {self.model_name}")
        try:
            from transformers import AutoImageProcessor, DetrForObjectDetection
            self.processor = AutoImageProcessor.from_pretrained(
                self.model_name,
                cache_dir=settings.CACHE_DIR,
            )
            self.model = DetrForObjectDetection.from_pretrained(
                self.model_name,
                cache_dir=settings.CACHE_DIR,
            )
            self.model = optimize_for_device(self.model, self.device)
        except Exception as e:
            print(f"Error loading model {self.model_name}: {str(e)}")
            raise e
    
    def answer(self, image):
        try:
            image = Image.open(BytesIO(image)).convert('RGB')
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
            target_sizes = torch.tensor([image.size[::-1]])
            target_sizes = target_sizes.to(self.device)
            results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)
            detections = []
            for score, label, box in zip(results[0]["scores"], results[0]["labels"], results[0]["boxes"]):
                box = [round(i, 2) for i in box.tolist()]
                detections.append({
                    "label": self.model.config.id2label[label.item()],
                    "confidence": round(score.item(), 3),
                    "box": box
                })
            return {
                'detections': detections,
                'model': self.model_name,
            }
        except Exception as e:
            print(f"Error during Object Detection: {str(e)}")
            raise e

__all__ = ['MultiModel', 'VisualQA', 'ImageCaptioning', 'OCRModel', 'ObjectDetectionModel']