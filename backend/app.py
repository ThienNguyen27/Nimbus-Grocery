from fastapi import FastAPI, HTTPException, File, UploadFile, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import StreamingResponse
from ultralytics import YOLO
import cv2
import numpy as np
import io

import os
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# Load environment variables from .env.local
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env.local"))

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
# Serve static files (e.g., signup.js)
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

# Configure templates directory
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# CORS middleware settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.68.62:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("../ml-models/grocery-detection-model/run/train/grocery_finetune5/weights/best.pt")

@app.get("/hello")
def read_hello():
    return "Hello World"

@app.get("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model.predict(frame, conf=0.4, iou=0.5)
    annotated = results[0].plot()

    _, img_encoded = cv2.imencode(".jpg", annotated)
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")

@app.get("/signup", response_class=HTMLResponse)
@app.get("/signup/", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# handle the form submission
@app.post("/signup")
async def post_signup(
    username: str = Form(...),
    email:    str = Form(...),
    password: str = Form(...),
):
    return {"status": "ok", "username": username, "email": email}