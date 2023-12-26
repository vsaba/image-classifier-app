from flask import Blueprint

hm = Blueprint('home', __name__, url_prefix='/home')


@hm.route('/', methods=['GET'])
def home():
    return "Hello world"
