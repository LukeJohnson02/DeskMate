from datetime import datetime

from sqlalchemy.orm import Session
from Models import User


class UserAdapter:
    """
    Adapter for database operations related to users.
    """

    def __init__(self, db: Session):
        """
        Initialise the UserAdapter with a database session.

        :param db: SQLAlchemy Session instance for database interaction.
        """
        self.db = db

    def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to fetch.
        :return: The User object if found, else None.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self):
        """
        Retrieve all users from the database.

        :return: A list of all User objects.
        """
        return self.db.query(User).all()

    def get_by_email(self, email: str):
        """
        Retrieve a user by their email address.

        :param email: The email address to search for.
        :return: The User object if found, else None.
        """
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, name: str, hashed_password: str, role: str):
        """
        Create a new user record in the database.

        :param email: The user's email address.
        :param name: The user's name.
        :param hashed_password: The user's hashed password.
        :param role: The role assigned to the user.
        :return: The newly created User object.
        """
        new_user = User(
            email=email, name=name, hashed_password=hashed_password, role=role
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user: User):
        """
        Commit updates to an existing user.

        :param user: The User object to update.
        :return: The updated User object.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        """
        Remove a user from the database.

        :param user: The User object to delete.
        """
        self.db.delete(user)
        self.db.commit()

    def set_reset_token(self, user: User, token: str, expiry: datetime):
        """
        Set a password reset token and its expiry for a user.

        :param user: The User object to update.
        :param token: The reset token string.
        :param expiry: The datetime when the token expires.
        """
        user.reset_token = token
        user.reset_token_expiry = expiry
        self.db.commit()
        self.db.refresh(user)

    def get_user_by_reset_token(self, token: str):
        """
        Retrieve a user by a valid reset token.

        :param token: The reset token string.
        :return: The User object if token is valid and not expired, else None.
        """
        now = datetime.now()
        return (
            self.db.query(User)
            .filter(User.reset_token == token, User.reset_token_expiry > now)
            .first()
        )

    def clear_reset_token(self, user: User):
        """
        Clear the password reset token and its expiry from a user.

        :param user: The User object to update.
        """
        user.reset_token = None
        user.reset_token_expiry = None
        self.db.commit()
        self.db.refresh(user)

    def update_password(self, user: User, hashed_password: str):
        """
        Update the hashed password for a user.

        :param user: The User object to update.
        :param hashed_password: The new hashed password.
        """
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
