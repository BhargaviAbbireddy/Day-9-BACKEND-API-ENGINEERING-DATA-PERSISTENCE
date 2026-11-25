
from sqlmodel import Session, select

from ticket_api.database import engine
from ticket_api.models import User, Ticket, Comment


def seed_database():
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == "alice@example.com")
        ).first()

        if not user:
            user = User(
                name="Alice Johnson",
                email="alice@example.com"
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        ticket = session.exec(
            select(Ticket).where(
                Ticket.title == "Sample Login Issue",
                Ticket.user_id == user.id
            )
        ).first()

        if not ticket:
            ticket = Ticket(
                title="Sample Login Issue",
                description="Unable to login to the application",
                status="open",
                priority="high",
                user_id=user.id
            )
            session.add(ticket)
            session.commit()
            session.refresh(ticket)

        comment = session.exec(
            select(Comment).where(
                Comment.content == "Please investigate this issue",
                Comment.ticket_id == ticket.id,
                Comment.user_id == user.id
            )
        ).first()

        if not comment:
            comment = Comment(
                content="Please investigate this issue",
                ticket_id=ticket.id,
                user_id=user.id
            )
            session.add(comment)
            session.commit()

    print("Synthetic seed data created successfully!")


if __name__ == "__main__":
    seed_database()
