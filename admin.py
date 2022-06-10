from flask import Blueprint
admin_page = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


@admin_page.route('/')
def home():
    return "admin home page"


@admin_page.route('/user')
def user():
    return "admin user page"