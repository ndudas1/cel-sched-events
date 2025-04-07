import os
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Database connection string
url = os.getenv('DATABASE_URL')
logging.info(f"Database URL: {url}")

engine = create_engine(url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_engine = SessionLocal()
