from config import engine
from models.base import Model  # Make sure base.Model is imported to ensure all models are registered
from models.user import User  # Ensure the User model is imported so that it gets registered

# Create the tables in the database
Model.metadata.create_all(engine)

print("Tables created successfully.")