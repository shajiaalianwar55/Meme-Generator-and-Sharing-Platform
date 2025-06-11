from flask import Blueprint
main = Blueprint('main',__name__)
@main.route('/')
def home():
    return "Hmm... you've discovered something special. Welcome to the Ultimate Meme Generator!"
