from models import *


class CategoryAccess:
    total_number = 0

    @classmethod
    def get_all_categories(cls):
        categories = Category.query.all()
        categories = [category.format() for category in categories]
        cls.total_number = len(categories)
        return categories
