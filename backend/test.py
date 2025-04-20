import logging
from sqlalchemy import text
from app.database.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test the database connection."""
    try:
        # Try to connect to the database and execute a simple query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            for row in result:
                logger.info(f"Connection successful: {row[0]}")
                
        logger.info("Database connection test completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()