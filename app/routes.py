# app/routes.py
from flask import Blueprint, request, jsonify
from app.models import User, Meme
from app.db import session_local   

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hmm... you've discovered something special. Welcome to the Ultimate Meme Generator!"


@main.route('/register', methods=['POST'])
def register():
    """
    POST /register
    Expects JSON: { "username": "...", "password": "..." }
    Creates a new User and returns its ID.
    """
    data = request.get_json()
    session = session_local()
    try:
        #1) build the User
        user = User(
            username      = data['username'],
            password_hash = data['password']
        )
        # 2) save
        session.add(user)
        session.commit()

        return jsonify({
            "message": "User created",
            "user_id":  user.id
        }), 201

    finally:
        session.close()


@main.route('/memes', methods=['GET'])
def list_memes():
    """
    GET /memes
    Returns a JSON array of every meme in the DB.
    """
    session = session_local()
    try:
        all_memes = session.query(Meme).all()
        result = [
            {
                "id":         m.id,
                "title":      m.title,
                "image_path": m.image_path,
                "likes":      m.likes
            }
            for m in all_memes
        ]
        return jsonify(result), 200

    finally:
        session.close()
