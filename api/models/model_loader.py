from . import orders, order_details, recipes, sandwiches, resources, promotions, reviews, customers
from ..dependencies.database import engine, Base  # Make sure Base is properly imported


def index():
    try:
        orders.Base.metadata.create_all(engine)
        order_details.Base.metadata.create_all(engine)
        recipes.Base.metadata.create_all(engine)
        sandwiches.Base.metadata.create_all(engine)
        resources.Base.metadata.create_all(engine)
        reviews.Base.metadata.create_all(engine)
        promotions.Base.metadata.create_all(engine)
        customers.Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
