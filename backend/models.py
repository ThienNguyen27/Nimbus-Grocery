from sqlalchemy import (Table, Column, Integer, String, Float, DateTime, MetaData, ForeignKey, Text)
import datetime

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("balance", Float, default=0.0),
    Column("face_embedding", Text, nullable=False),  # serialized 128-d vector
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)

item_checklist = Table(
    "item_checklist", metadata,
    Column("item_id", Integer, primary_key=True),
    Column("item_name", String(255)),
    Column("quantity_remaining", Integer),
    Column("price", Float),
    Column("last_updated", DateTime, default=datetime.datetime.utcnow),
)

user_transactions = Table(
    "user_transactions", metadata,
    Column("transaction_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("amount", Float),
    Column("description", String(255), nullable=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
    Column("balance", Float),
    Column("total_quantity", Integer, nullable=False, server_default="0"),
)

transaction_items = Table(
    "transaction_items", metadata,
    Column("transaction_item_id", Integer, primary_key=True),
    Column("transaction_id", Integer, ForeignKey("user_transactions.transaction_id")),
    Column("item_id", Integer, ForeignKey("item_checklist.item_id")),
    Column("quantity", Integer),
    Column("price", Float),
)
