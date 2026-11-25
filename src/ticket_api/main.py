
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from ticket_api.database import get_session
from ticket_api.models import User
from ticket_api.schemas import UserCreate, UserResponse

from datetime import datetime, timezone
from typing import Literal

from fastapi import Query, Response

from ticket_api.models import Ticket
from ticket_api.schemas import TicketCreate, TicketUpdate, TicketResponse

from ticket_api.models import Comment
from ticket_api.schemas import CommentCreate, CommentResponse

app = FastAPI(
    title="Ticket Management API",
    description="API for managing users, tickets and comments",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Ticket Management API is running"}


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.get("/users", response_model=list[UserResponse])
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(
    ticket_data: TicketCreate,
    session: Session = Depends(get_session)
):
    user = session.get(User, ticket_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ticket = Ticket.model_validate(ticket_data)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket


@app.get("/tickets", response_model=list[TicketResponse])
def get_tickets(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    status: str | None = None,
    priority: str | None = None,
    session: Session = Depends(get_session)
):
    statement = select(Ticket)

    if status:
        statement = statement.where(Ticket.status == status)

    if priority:
        statement = statement.where(Ticket.priority == priority)

    statement = statement.offset(skip).limit(limit)

    return session.exec(statement).all()


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = ticket_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ticket, key, value)

    ticket.updated_at = datetime.now(timezone.utc)

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket


@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    session.delete(ticket)
    session.commit()

    return Response(status_code=204)


@app.post(
    "/tickets/{ticket_id}/comments",
    response_model=CommentResponse,
    status_code=201
)
def create_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    user = session.get(User, comment_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    comment = Comment(
        content=comment_data.content,
        ticket_id=ticket_id,
        user_id=comment_data.user_id
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment


@app.get(
    "/tickets/{ticket_id}/comments",
    response_model=list[CommentResponse]
)
def get_ticket_comments(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    ticket = session.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    statement = select(Comment).where(Comment.ticket_id == ticket_id)

    return session.exec(statement).all()
