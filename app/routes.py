from flask import Blueprint, request, jsonify
from app.models import User, Meme
from app.models import db 

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
    try:
        user = User(
            username=data['username'],
            password_hash=data['password']
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User created",
            "user_id": user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@main.route('/memes', methods=['GET'])
def list_memes():
    """
    GET /memes
    Returns a JSON array of every meme in the DB.
    """
    try:
        all_memes = db.session.query(Meme).all()
        result = [
            {
                "id": m.id,
                "title": m.title,
                "image_path": m.image_path,
                "likes": m.likes
            }
            for m in all_memes
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
