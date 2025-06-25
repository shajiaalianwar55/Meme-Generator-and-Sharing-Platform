from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models import User, Meme
from app.models import db
from app.utils import add_caption
import os

main = Blueprint('main', __name__)

# 1. Define allowed extensions in one place
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@main.route('/')
def home():
    return "Hmm... you've discovered something special. Welcome to the Ultimate Meme Generator!"

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Both username and password are required'}), 400

    try:
        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'User created',
            'user_id': user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/memes', methods=['GET'])
def list_memes():
    try:
        memes = Meme.query.all()
        result = []
        for meme in memes:
            meme_data= {
                'id': meme.id,
                'title':meme.title,
                'image_path':meme.image_path,
                'likes':meme.likes,
                'created_at':meme.created_at.isoformat(),
                'username':meme.user.username
            }
            result.append(meme_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No file uploaded, Retry'}), 400
    if file.filename == '':
        return jsonify({'error': 'No file selected, Retry'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported, Retry'}), 415

    filename = secure_filename(file.filename)
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    # Return a client‐friendly URL
    url_path = f'/static/uploads/{filename}'
    return jsonify({
        'message': 'Upload successful',
        'file_path': url_path
    }), 201

@main.route('/create-meme', methods=['POST'])
def create_meme():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded, Retry'}), 400
    if file.filename == '':
        return jsonify({'error': 'No image selected, Retry'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported, Retry'}), 415

    top_text = request.form.get('top_text', '')
    bottom_text = request.form.get('bottom_text', '')
    title = request.form.get('title', 'Untitled')

    # 2. Save the original upload
    filename = secure_filename(file.filename)
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    original_path = os.path.join(upload_folder, filename)
    file.save(original_path)

    # 3. Generate the captioned image
    #    (assumes add_caption returns a PIL Image object)
    meme_img = add_caption(original_path, top_text, bottom_text)

    # 4. Ensure we have a file extension (default to .png)
    name, ext = os.path.splitext(filename)
    ext = ext if ext else '.png'
    meme_filename = f'meme_{name}{ext}'

    # 5. Save your new meme into static/memes
    meme_folder = os.path.join(os.path.dirname(__file__), 'static', 'memes')
    os.makedirs(meme_folder, exist_ok=True)
    meme_path = os.path.join(meme_folder, meme_filename)
    meme_img.save(meme_path)

    # 6. Store a *URL* in the DB, not the absolute disk path
    url_path = f'/static/memes/{meme_filename}'
    meme_entry = Meme(user_id=1, image_path=url_path, title=title)
    db.session.add(meme_entry)
    db.session.commit()

    return jsonify({
        'message': 'Meme created successfully',
        'id': meme_entry.id,
        'path': url_path,
        'title': meme_entry.title
    }), 201
    
@main.route('/memes/<int:meme_id>/like', methods = ['POST'])
def like_meme(meme_id):
    meme=Meme.query.get(meme_id)
    if meme is not None:
        meme.likes+=1
        db.session.commit()
        return jsonify({'message' : 'like added', 'meme_likes' : meme.likes}),200
    else:
        return jsonify({'error':'Meme does not exist'}),404