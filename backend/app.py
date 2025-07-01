# uvicorn app:app --reload
from fastapi.middleware.cors import CORSMiddleware
import os, sys
from dotenv import load_dotenv
from models import *
from schemas import *
from databases import Database
from sqlalchemy import create_engine, select, update, insert
from sqlalchemy.orm import sessionmaker, Session
import bcrypt
import uuid
import traceback
import logging
logger = logging.getLogger("uvicorn.error")
from fastapi import FastAPI, HTTPException, File, UploadFile, Request, Form,  Depends
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
import face_recognition
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_models.person_detection_model.model import load_known_faces, safe_face_encodings
import json

# Load environment variables from .env.local
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env.local"))
DATABASE_URL = os.getenv("DATABASE_URL")

# Create sync engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Create tables if not exist 
metadata.create_all(engine)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "welcome to nimbus!"}

@app.post("/signup", response_model=UserResponse)
async def signup(
    name: str            = Form(...),
    email: str           = Form(...),
    password: str        = Form(...),
    photo: UploadFile = File(...),
    db: Session          = Depends(get_db),
):
    try:
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Hash face id
        img_bytes = await photo.read()
        nparr     = np.frombuffer(img_bytes, np.uint8)
        bgr_img   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img   = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

        # detect & encode faces
        face_locations = face_recognition.face_locations(rgb_img)
        encodings      = safe_face_encodings(rgb_img, face_locations)
        if not encodings:
            raise HTTPException(400, "Could not detect a face in the uploaded photo.")

        # serialize the first 128-dim embedding as JSON
        face_embedding = encodings[0].tolist()
        face_id_hash   = json.dumps(face_embedding)
        

        result = db.execute(
            insert(users).values(
                name = name,
                email= email,
                password_hash=hashed_password,
                face_id_hash = face_id_hash,
                balance = 100.0
            )
        )
        logger.info("result %s", result)
        db.commit()
        user_id = result.inserted_primary_key[0]

        user = db.execute(select(users).where(users.c.user_id == user_id)).fetchone()
        if not user:
            raise HTTPException(status_code=500, detail="User creation failed")
        return UserResponse(**dict(user._mapping))

    except Exception as e:
        traceback.print_exc()  # this prints the full error stack trace to your terminal
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/buy")
def buy(request: BuyRequest, db=Depends(get_db)):
    user = db.execute(select(users).where(users.c.user_id == request.user_id)).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for item in request.items:
        db_item = db.execute(select(item_checklist).where(item_checklist.c.item_id == item.item_id)).fetchone()
        if not db_item or db_item.quantity_remaining < item.quantity:
            raise HTTPException(status_code=400, detail=f"Item {item.item_id} unavailable")
        db.execute(
            update(item_checklist)
            .where(item_checklist.c.item_id == item.item_id)
            .values(quantity_remaining=db_item.quantity_remaining - item.quantity)
        )
    db.commit()
    return {"message": "Items reserved"}

@app.post("/pay", response_model=TransactionResponse)
def pay(request: PayRequest, db=Depends(get_db)):
    user = db.execute(select(users).where(users.c.user_id == request.user_id)).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.balance < request.total_amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    new_balance = user.balance - request.total_amount
    db.execute(update(users).where(users.c.user_id == request.user_id).values(balance=new_balance))

    result = db.execute(
        insert(user_transactions).values(
            user_id=request.user_id,
            amount=-request.total_amount,
            description=request.description,
            balance=new_balance,
        )
    )
    transaction_id = result.inserted_primary_key[0]

    items_responses = []
    for item in request.items:
        res = db.execute(
            insert(transaction_items).values(
                transaction_id=transaction_id,
                item_id=item.item_id,
                quantity=item.quantity,
                price=item.price,
            )
        )
        trans_item_id = res.inserted_primary_key[0]
        items_responses.append(TransactionItemResponse(
            transaction_item_id=trans_item_id,
            transaction_id=transaction_id,
            item_id=item.item_id,
            quantity=item.quantity,
            price=item.price,
        ))
    db.commit()

    transaction = db.execute(select(user_transactions).where(user_transactions.c.transaction_id == transaction_id)).fetchone()
    return TransactionResponse(
        transaction_id=transaction.transaction_id,
        amount=transaction.amount,
        description=transaction.description,
        created_at=transaction.created_at,
        balance=transaction.balance,
        items=items_responses,
    )

@app.get("/users")
def get_all_users(db=Depends(get_db)):
    # SELECT * FROM users
    query = select(users)
    result = db.execute(query).mappings().all()


    # Convert result rows to dictionaries for JSON response
    users_list = [dict(row) for row in result]

    return {"users": users_list}

@app.get("/test")
def test():
    logger.info("Test endpoint was called!")
    return {"message": "Test successful"}
# CORS middleware settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("../ml_models/grocery-detection-model/run/train/grocery_finetune5/weights/best.pt")

@app.get("/hello")
def read_hello():
    return "Hello World"


# detect groceries 
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model.predict(frame, conf=0.4, iou=0.5)
    annotated = results[0].plot()

    _, img_encoded = cv2.imencode(".jpg", annotated)
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")

# detect peron
@app.post("/predict-person")
async def predictBuyer(file: UploadFile = File(...)):
    return


@app.get("/signup", response_class=HTMLResponse)
@app.get("/signup/", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
