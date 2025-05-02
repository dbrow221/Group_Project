from ..dependencies.database import Base, engine

# Explicitly import all models to register them with Base
from .orders import Order
from .order_details import OrderDetail
from .recipes import Recipe
from .sandwiches import Sandwich
from .resources import Resource
from .promotions import Promotion
from .reviews import Review
from .customers import Customer

def index():
    try:
        Base.metadata.drop_all(engine)   # optional: to reset DB
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
