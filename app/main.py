from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.endpoints import router
from app.model_instance import model_vqa, model_captioning, model_ocr, model_object_detection

app = FastAPI(title="Multimodal Demo")
#app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(router, prefix='/api')

@app.on_event("startup")
async def startup_event():
    model_vqa.load_model()
    model_captioning.load_model()
    model_ocr.load_model()
    model_object_detection.load_model()

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})