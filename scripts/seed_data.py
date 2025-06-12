from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import User, Meme

engine = create_engine('sqlite:///data/database.db')
Session = sessionmaker(bind=engine)
session = Session()

#Create a test user
test_user = User(username = "person", password_hash ="test123")
session.add(test_user)
session.commit()

#Create a meme for the test user
test_meme = Meme(user_id=test_user.id, image_path="memes/new_meme.png", title = "My first meme, Woohoo", likes =45)
session.add(test_meme)
session.commit()

print("Test user and meme added successfully!")

#Test: Fetch all users
users = session.query(User).all()
for user in users:
  print(f"User:{user.username}")

#Test: Fetch all memes
memes = session.query(Meme).all()
for meme in memes:
  print(f"Meme: {meme.title}, Likes : {meme.likes}")