"""Category workflow orchestration for support ticket classification."""

from Database.Adapters.category_adapter import CategoryAdapter


class CategoryController:
    """
    Controller responsible for handling operations related to categories.
    """

    def __init__(self, adapter: CategoryAdapter):
        """
        Initialize the CategoryController with a CategoryAdapter.

        :param adapter: An instance of CategoryAdapter to interact with category data.
        """
        self.adapter = adapter

    def fetch_categories(self):
        """
        Retrieve all categories from the database.

        :return: A list of all category records.
        """
        return self.adapter.get_all_categories()

    def fetch_category(self, category_id: int):
        """
        Retrieve a specific category by its ID.

        :param category_id: The ID of the category to fetch.
        :return: The category record if found.
        :raises ValueError: If the category is not found.
        """
        category = self.adapter.get_category_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        return category
