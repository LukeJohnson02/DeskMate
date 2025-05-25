from Database.Adapters.category_adapter import CategoryAdapter


class CategoryController:
    def __init__(self, adapter: CategoryAdapter):
        self.adapter = adapter

    def fetch_categories(self):
        return self.adapter.get_all_categories()

    def fetch_category(self, category_id: int):
        category = self.adapter.get_category_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        return category
