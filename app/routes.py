from flask import Blueprint, request, jsonify
from app.models import User, Meme
from app.models import db 
from werkzeug.utils import secure_filename
import os

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in {'png','jpg','jpeg'}

@main.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded, Retry'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected, Retry'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File Type not supported, Retry'}), 415

    filename = secure_filename(file.filename)
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    return jsonify({
        "message": "Upload successful",
        "file_path": f"/static/uploads/{filename}"
    }), 201

    
