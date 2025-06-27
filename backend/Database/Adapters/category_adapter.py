from sqlalchemy.orm import Session
from Models import Category


class CategoryAdapter:
    """
    Adapter for performing database operations related to categories.
    """

    def __init__(self, db: Session):
        """
        Initialise the CategoryAdapter with a database session.

        :param db: SQLAlchemy Session instance for database interaction.
        """
        self.db = db

    def get_all_categories(self):
        """
        Retrieve all categories from the database.

        :return: A list of all Category objects.
        """
        return self.db.query(Category).all()

    def get_category_by_id(self, category_id: int):
        """
        Retrieve a single category by its ID.

        :param category_id: The ID of the category to fetch.
        :return: The Category object if found, else None.
        """
        return self.db.query(Category).filter(Category.id == category_id).first()

    def create_category(self, category: Category):
        """
        Add a new category to the database.

        :param category: The Category object to add.
        :return: The newly created Category object.
        """
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
