from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

ENGINE = create_engine('sqlite:///data/database.db', echo=True)

session_local = sessionmaker(bind=ENGINE,autoflush = False,autocommit=False)

Base.metadata.create_all(ENGINE)
