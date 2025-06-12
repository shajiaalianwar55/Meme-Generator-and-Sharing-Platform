from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key = True )
  username = Column (String, nullable = False )
  password_hash = Column (String(255), nullable = False)

  memes = relationship("Meme", back_populates ="user")

class Meme(Base):
  __tablename__ = 'memes'
  id = Column(Integer, primary_key =True)
  user_id = Column(Integer, ForeignKey('users.id'))
  image_path = Column(String(255), nullable=False)
  title = Column(String(255), nullable=False)
  created_at= Column(DateTime(timezone=True), default =datetime.utcnow)
  likes = Column(Integer, default =0)
  user = relationship("User",back_populates="memes")