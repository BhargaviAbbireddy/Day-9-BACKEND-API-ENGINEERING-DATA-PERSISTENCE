from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    status: Literal["open", "in_progress", "closed"] = "open"
    priority: Literal["low", "medium", "high"] = "medium"
    user_id: int


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    status: Literal["open", "in_progress", "closed"] | None = None
    priority: Literal["low", "medium", "high"] | None = None


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    user_id: int


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    ticket_id: int
    user_id: int
    created_at: datetime
