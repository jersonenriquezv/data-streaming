from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional 


class Transaction(BaseModel):
    amount: float = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(..., min_length=3, max_length=20)
    transaction_id: Optional[str] = None

