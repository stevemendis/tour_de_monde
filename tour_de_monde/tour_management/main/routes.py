from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # return "Hello World"
    return render_template('user/index.html')