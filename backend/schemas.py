from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserResponse(BaseModel):
    user_id: int
    name: str
    balance: float
    face_embedding: Optional[str] = None
    created_at: datetime

class BuyItem(BaseModel):
    item_id: int
    quantity: int

class BuyRequest(BaseModel):
    user_id: int
    items: List[BuyItem]

class PayItem(BaseModel):
    item_id: int
    quantity: int
    price: float

class PayRequest(BaseModel):
    user_id: int
    items: List[PayItem]
    total_amount: float
    description: Optional[str] = None

class TransactionItemResponse(BaseModel):
    transaction_item_id: int
    transaction_id: int
    item_id: int
    quantity: int
    price: float

class TransactionResponse(BaseModel):
    transaction_id: int
    amount: float
    description: Optional[str]
    created_at: datetime
    balance: float
    items: List[TransactionItemResponse]

class TokenResponse(BaseModel):
    token: str

class PredictResponse(BaseModel):
    name: str