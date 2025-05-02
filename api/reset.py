# reset_db.py

from api.dependencies.database import Base, engine
from api.models import orders, order_details, recipes, sandwiches, resources, promotions, reviews, customers

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()
