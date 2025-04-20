from app.database.session import engine, Base 
from app.models.user import User

def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
    # Optionally, you can add more tables here if needed
    
if __name__ == "__main__":
    create_tables()
    # print("Database tables created successfully.")