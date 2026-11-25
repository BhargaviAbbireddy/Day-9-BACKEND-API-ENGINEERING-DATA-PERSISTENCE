from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    __tablename__ = "users"

    tickets: list["Ticket"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    __tablename__ = "tickets"
    description: Optional[str] = None
    status: str = "open"
    priority: str = "medium"
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: Optional[User] = Relationship(back_populates="tickets")
    comments: list["Comment"] = Relationship(back_populates="ticket")


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    __tablename__ = "comments"
    ticket_id: int = Field(foreign_key="tickets.id")
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    ticket: Optional[Ticket] = Relationship(back_populates="comments")
    user: Optional[User] = Relationship(back_populates="comments")
