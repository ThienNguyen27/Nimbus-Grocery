from fastapi import FastAPI, HTTPException,Request 
from fastapi.middleware.cors import CORSMiddleware

import os
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# Load environment variables from .env.local
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env.local"))

app = FastAPI()
# Serve static files (e.g., signup.js)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Configure templates directory
templates = Jinja2Templates(directory="templates")
# CORS middleware settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/hello")
def read_hello():
    return "Hello World"

@app.get("/predict")
def predict():
    return "Predict"
@app.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})