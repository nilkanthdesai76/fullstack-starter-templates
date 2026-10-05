from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os

app = FastAPI(
    title="Production FastAPI Starter",
    description="High-performance async API with health checks, structured schemas, and CORS",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))

class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)

class ItemResponse(ItemCreate):
    id: int

# In-memory store for demo
_db: List[ItemResponse] = []

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    return HealthResponse()

@app.get("/api/v1/items", response_model=List[ItemResponse], tags=["Items"])
async def list_items():
    return _db

@app.post("/api/v1/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate):
    new_id = len(_db) + 1
    created = ItemResponse(id=new_id, **item.model_dump())
    _db.append(created)
    return created

@app.get("/api/v1/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(item_id: int):
    for item in _db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
