import pytest
from app import create_app, db

@pytest.fixture
def app():
    test_app = create_app(test_config={
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()

def test_user_creation(app):
    from app.models import User

    user = User(username="shajiaali", password_hash="dummy_pass")
    db.session.add(user)
    db.session.commit()

    found_user = User.query.filter_by(username="shajiaali").first()
    assert found_user is not None
    assert found_user.username == "shajiaali"

def test_meme_creation(app):
    from app.models import User, Meme

    user = User(username="shajia", password_hash="secret")
    db.session.add(user)
    db.session.commit()

    meme = Meme(
        user_id=user.id,
        title="test meme",
        image_path="memesssssssss/test.jpg" 
    )
    db.session.add(meme)
    db.session.commit()

    found_meme = Meme.query.filter_by(title="test meme").first()
    assert found_meme is not None
    assert found_meme.user_id == user.id
    assert found_meme.title == "test meme"
