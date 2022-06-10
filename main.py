import requests
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from admin import admin_page


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'firstweb'


class Register(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), nullable=False)
    password = db.Column('password', db.String(50), nullable=False)


db.create_all()

url = "https://www.fishwatch.gov/api/species"
r = requests.get(url)
data = r.json()




def __str__(self):
    return f'Username: {self.username},  Password: {self.password}'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        password = request.form["password"]
        if Register.query.filter_by(username=name, password=password).first():
            session['user'] = name
            return redirect(url_for("user"))
        flash("Username or Password is invalid")
        return render_template("login.html")
    if request.method == "GET":
        return render_template("login.html")


@app.route('/user')
def user(name=None):
    if 'user' in session:
        name = session['user']
        return render_template('user.html')
    else:
        return f'hello {name}'


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/discover')
def discover():
    return render_template('disc.html', data=data)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        session.permanent = True
        name = request.form['name']
        password = request.form['password']
        if len(name) == 0:
            flash("Name field is empty")
            return render_template("registration.html")

        elif len(password) == 0:
            flash("Password field is empty")
            return render_template("registration.html")

        elif len(name) < 6:
            flash("Name should be more than 5 characters")
            return render_template("registration.html")

        elif len(password) < 6:
            flash("Password should be more than 5 characters")
            return render_template("registration.html")

        if Register.query.filter_by(username=name).first():
            flash("Username already exist")
            return render_template("registration.html")

        else:
            user_info = Register(username=name, password=password)
            session.permanent = True
            session['user'] = name
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('user'))
    return render_template("registration.html")


if __name__ == '__main__':
    app.run(debug=True)
