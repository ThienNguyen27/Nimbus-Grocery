# uvicorn app:app --reload
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from models import *
from schemas import *
from databases import Database
from sqlalchemy import create_engine, select, update, insert
from sqlalchemy.orm import sessionmaker
import bcrypt
import uuid
import traceback
import logging
logger = logging.getLogger("uvicorn.error")

# Load environment variables from .env.local
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env.local"))
DATABASE_URL = os.getenv("DATABASE_URL")

# Create sync engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Create tables if not exist 
metadata.create_all(engine)

app = FastAPI()

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
def signup(data: UserSignupRequest, db=Depends(get_db)):
    try:
        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        random_face_id = str(uuid.uuid4())
        face_id = data.face_id_hash or random_face_id

        result = db.execute(
            insert(users).values(
                name=data.name,
                email=data.email,
                password_hash=hashed_password,
                face_id_hash=face_id,
                balance=100.0
            )
        )
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