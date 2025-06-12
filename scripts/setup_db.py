from sqlalchemy import create_engine
from app.models import Base

engine=create_engine('sqlite:///data/database.db')
Base.metadata.create_all(engine)