from sqlalchemy import create_engine            
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Creating database url
SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"
# Creating new database connections for us (which also holds onto conenctions inside of a connection pool)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)      
conn = engine.connect()

# session maker generates new session objects when called
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     
Base = declarative_base()       # create a base class for declarative class def