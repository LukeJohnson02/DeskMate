from sqlalchemy.orm import Session
from Authentication.Utils.security import hash_password
from Database.database import Base, engine, SessionLocal
from Models import Ticket, Category, User, UserRole
from Models.ticket_model import TicketStatus


def populate_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Clear existing data (optional)
        db.query(Ticket).delete()
        db.query(Category).delete()
        db.query(User).delete()
        db.commit()

        # Create users with roles using Enum
        users = [
                    User(
                        name=f"user{i}",
                        email=f"user{i}@example.com",
                        hashed_password=hash_password("password123"),
                        role=UserRole.USER,
                        is_verified=True  # Mark as verified for testing
                    )
                    for i in range(1, 8)
                ] + [
                    User(
                        name=f"admin{i}",
                        email=f"admin{i}@example.com",
                        hashed_password=hash_password("adminpass123"),
                        role=UserRole.ADMIN,
                        is_verified=True  # Also mark admins as verified
                    )
                    for i in range(1, 4)
                ]

        db.add_all(users)
        db.commit()

        # Create categories
        categories = [
            Category(name=f"Category {i}")
            for i in range(1, 11)
        ]
        db.add_all(categories)
        db.commit()

        # Create tickets with proper Enum status and link to users/categories
        tickets = []
        status_cycle = [TicketStatus.OPEN, TicketStatus.IN_PROGRESS, TicketStatus.CLOSED]

        for i in range(1, 11):
            ticket = Ticket(
                title=f"Ticket {i}",
                description=f"This is the description for ticket {i}.",
                status=status_cycle[i % 3],  # cycle through statuses
                user_id=users[i % len(users)].id,
                category_id=categories[i % len(categories)].id,
            )
            tickets.append(ticket)

        db.add_all(tickets)
        db.commit()

        print("Database populated successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()