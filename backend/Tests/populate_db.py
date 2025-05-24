from sqlalchemy.orm import Session

from Database.database import Base, engine, SessionLocal
from Models import Ticket, Category, User, UserRole


def populate_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Clear existing data (optional)
    db.query(Ticket).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()

    # Create Users
    users = [
        User(name="Admin 1", email="admin1@it.com", role=UserRole.ADMIN.value),
        User(name="Admin 2", email="admin2@it.com", role=UserRole.ADMIN.value),
    ] + [
        User(name=f"User {i}", email=f"user{i}@it.com", role=UserRole.USER.value)
        for i in range(1, 9)
    ]
    db.add_all(users)
    db.commit()

    # Create Categories
    categories = [Category(name=f"Category {i}") for i in range(1, 11)]
    db.add_all(categories)
    db.commit()

    # Create Tickets
    tickets = [
        Ticket(
            title=f"Ticket {i}",
            description=f"Description of ticket {i}",
            user_id=((i % 8) + 3),       # Assign tickets to users (id 3 to 10)
            category_id=((i - 1) % 10) + 1,
            status="open" if i % 2 == 0 else "in_progress"
        ) for i in range(1, 11)
    ]
    db.add_all(tickets)
    db.commit()

    db.close()

if __name__ == "__main__":
    populate_db()
