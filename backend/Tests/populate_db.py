"""Populate the local development database with realistic demo data."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from Authentication.Utils.security import hash_password
from Database.database import Base, engine, SessionLocal
from Models import Ticket, Category, User, UserRole
from Models.ticket_model import TicketStatus


@dataclass(frozen=True)
class DemoUser:
    name: str
    email: str
    password: str
    role: UserRole


@dataclass(frozen=True)
class DemoTicket:
    title: str
    description: str
    status: TicketStatus
    user_email: str
    category_name: str


DEMO_USERS = [
    DemoUser("Maya Patel", "user1@example.com", "password123", UserRole.USER),
    DemoUser("Ethan Brooks", "ethan.brooks@example.com", "password123", UserRole.USER),
    DemoUser("Nora Williams", "nora.williams@example.com", "password123", UserRole.USER),
    DemoUser("Leo Chen", "leo.chen@example.com", "password123", UserRole.USER),
    DemoUser("Amelia Johnson", "amelia.johnson@example.com", "password123", UserRole.USER),
    DemoUser("Sam Rivera", "sam.rivera@example.com", "password123", UserRole.USER),
    DemoUser("Priya Singh", "priya.singh@example.com", "password123", UserRole.USER),
    DemoUser("Grace Miller", "admin1@example.com", "adminpass123", UserRole.ADMIN),
    DemoUser("Owen Clarke", "owen.clarke@example.com", "adminpass123", UserRole.ADMIN),
    DemoUser("Isla Morgan", "isla.morgan@example.com", "adminpass123", UserRole.ADMIN),
]


CATEGORY_NAMES = [
    "Hardware",
    "Software",
    "Network",
    "Account Access",
    "Email",
    "Facilities",
    "Security",
    "Onboarding",
    "Payroll",
    "Mobile Devices",
]


DEMO_TICKETS = [
    DemoTicket(
        "Laptop fan is constantly running",
        "The device gets hot during video calls and the fan stays at full speed even after closing all applications.",
        TicketStatus.OPEN,
        "user1@example.com",
        "Hardware",
    ),
    DemoTicket(
        "Need access to finance shared drive",
        "I joined the month-end reporting project and need read/write access to the finance shared drive before Friday.",
        TicketStatus.IN_PROGRESS,
        "ethan.brooks@example.com",
        "Account Access",
    ),
    DemoTicket(
        "VPN disconnects after ten minutes",
        "The VPN connects successfully from home but drops after about ten minutes, interrupting remote desktop sessions.",
        TicketStatus.OPEN,
        "nora.williams@example.com",
        "Network",
    ),
    DemoTicket(
        "New starter laptop setup",
        "Please prepare a standard laptop build with Teams, Office, browser profiles, and security tools for a new analyst.",
        TicketStatus.IN_PROGRESS,
        "leo.chen@example.com",
        "Onboarding",
    ),
    DemoTicket(
        "Outlook mailbox search not returning recent mail",
        "Search results stop at last month even though the messages are visible in the inbox and folders.",
        TicketStatus.OPEN,
        "amelia.johnson@example.com",
        "Email",
    ),
    DemoTicket(
        "Conference room display has no signal",
        "The large display in meeting room 3B shows no signal when connected over HDMI or wireless casting.",
        TicketStatus.CLOSED,
        "sam.rivera@example.com",
        "Facilities",
    ),
    DemoTicket(
        "Password manager browser extension missing",
        "The approved password manager extension disappeared after the latest browser update and cannot be reinstalled manually.",
        TicketStatus.OPEN,
        "priya.singh@example.com",
        "Security",
    ),
    DemoTicket(
        "Payroll portal rejects MFA code",
        "The payroll portal accepts my password but rejects the current MFA code every time I try to download payslips.",
        TicketStatus.IN_PROGRESS,
        "user1@example.com",
        "Payroll",
    ),
    DemoTicket(
        "Phone will not sync calendar",
        "Company calendar events stopped syncing to the managed iPhone yesterday, but email still arrives normally.",
        TicketStatus.OPEN,
        "ethan.brooks@example.com",
        "Mobile Devices",
    ),
    DemoTicket(
        "Design software license renewal",
        "The design application says the license expires this week and blocks export features needed for a client presentation.",
        TicketStatus.CLOSED,
        "nora.williams@example.com",
        "Software",
    ),
    DemoTicket(
        "Guest Wi-Fi captive portal loop",
        "Visitors can connect to guest Wi-Fi but the captive portal keeps reloading after they accept the terms.",
        TicketStatus.OPEN,
        "leo.chen@example.com",
        "Network",
    ),
    DemoTicket(
        "Admin approval needed for database tool",
        "The installer for the approved database client prompts for administrator approval during setup.",
        TicketStatus.IN_PROGRESS,
        "amelia.johnson@example.com",
        "Software",
    ),
    DemoTicket(
        "Badge reader intermittent at side entrance",
        "The side entrance reader often flashes red for valid staff badges, especially during the morning rush.",
        TicketStatus.CLOSED,
        "sam.rivera@example.com",
        "Facilities",
    ),
    DemoTicket(
        "Suspicious email reported",
        "I received a message asking me to confirm payroll details through an unfamiliar link and need it reviewed.",
        TicketStatus.OPEN,
        "priya.singh@example.com",
        "Security",
    ),
    DemoTicket(
        "Shared mailbox permissions update",
        "Please remove two former team members and add the new coordinator to the customer success shared mailbox.",
        TicketStatus.CLOSED,
        "user1@example.com",
        "Email",
    ),
]


def populate_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Reset local demo data so repeated runs produce the same useful dataset.
        db.query(Ticket).delete()
        db.query(Category).delete()
        db.query(User).delete()
        db.commit()

        users = [
            User(
                name=user.name,
                email=user.email,
                hashed_password=hash_password(user.password),
                role=user.role,
                is_verified=True,
            )
            for user in DEMO_USERS
        ]

        db.add_all(users)
        db.commit()

        categories = [Category(name=name) for name in CATEGORY_NAMES]
        db.add_all(categories)
        db.commit()

        users_by_email = {user.email: user for user in users}
        categories_by_name = {category.name: category for category in categories}
        tickets = [
            Ticket(
                title=ticket.title,
                description=ticket.description,
                status=ticket.status,
                user_id=users_by_email[ticket.user_email].id,
                category_id=categories_by_name[ticket.category_name].id,
            )
            for ticket in DEMO_TICKETS
        ]

        db.add_all(tickets)
        db.commit()

        print("Database populated successfully.")
        print("Demo admin: admin1@example.com / adminpass123")
        print("Demo user: user1@example.com / password123")
        print(
            f"Created {len(users)} users, {len(categories)} categories, "
            f"and {len(tickets)} tickets."
        )

    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    populate_db()
