from sqlalchemy.orm import Session
from api.models.sandwiches import Sandwich
from api.models.recipes import Recipe
from api.models.customers import Customer  # Assuming you have a Customer model
from api.dependencies.database import SessionLocal


def seed_database():
    db: Session = SessionLocal()

    # Check if the database is already seeded
    if db.query(Sandwich).first() or db.query(Recipe).first() or db.query(Customer).first():
        print("Database already seeded.")
        return

    # Add sandwiches and recipes
    turkey_sandwich = Sandwich(sandwich_name="Turkey Sandwich", price=5.99, description="A delicious turkey sandwich.")
    turkey_recipe = Recipe(
        id=turkey_sandwich.id,
        ingredients="Turkey, Lettuce, Bread, Cheese"
    )
    turkey_sandwich.recipe = turkey_recipe

    veggie_sandwich = Sandwich(sandwich_name="Veggie Sandwich", price=4.99, description="A healthy veggie sandwich.")
    veggie_recipe = Recipe(
        id=veggie_sandwich.id,
        ingredients="Lettuce, Tomato, Bread, Cheese"
    )
    veggie_sandwich.recipe = veggie_recipe

    chicken_sandwich = Sandwich(sandwich_name="Chicken Sandwich", price=6.99, description="A crispy chicken sandwich.")
    chicken_recipe = Recipe(
        id=chicken_sandwich.id,
        ingredients="Chicken, Lettuce, Bread, Mayo"
    )
    chicken_sandwich.recipe = chicken_recipe

    db.add_all([turkey_sandwich, veggie_sandwich, chicken_sandwich])
    db.commit()

    # Add customers
    customer1 = Customer(name="John Doe", email="john@example.com", phone="123-456-7890")
    customer2 = Customer(name="Jane Smith", email="jane@example.com", phone="987-654-3210")
    customer3 = Customer(name="Bob Brown", email="bob@example.com", phone="555-555-5555")

    db.add_all([customer1, customer2, customer3])
    db.commit()

    print("Database seeded with sandwiches, recipes, and customers.")

if __name__ == "__main__":
    seed_database()