from models import Base, User
import bcrypt

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, or_

from flask import Flask, render_template, request, redirect
app = Flask(__name__)


engine = create_engine('sqlite:///users_info.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Putting it all together.
# Create a route to capture: '/login or /signup'
# Username
# email
# password - Encrypted - you choose
# Keep track of login attempts per username
# Did the user forget their password?
# Limit to 5 logins. Otherwise lock account
# At the server keep track of the total number of unique logins
# Use SQLAlchemy to store the database objects
# USe SQLite to store the data.


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return render_template('login_register.html')


@app.route('/test2')
def test2():
    return render_template('test2.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            res = request.form.to_dict()
            hashed = bcrypt.hashpw(
                res['password'].encode('utf8'), bcrypt.gensalt())
            if res['username'] == '':
                raise Exception('username cannot be empty')
            foundUser = session.query(User).filter(
                User.username == res['username']).first()

            if not foundUser:
                raise Exception('Login and password don\'t match')
            if bcrypt.checkpw(res['password'].encode('utf8'), hashed):
                if foundUser.login_count > 4:
                    raise Exception('Login restricted')
                foundUser.login_count += 1
                session.commit()
                return f"<h2>Welcome, {res['username']}. Your login count is {foundUser.login_count}</h2><a href='/'>back</a>"
            else:
                raise Exception('Password doesn\'t match')
        except Exception as error:
            return f"<h2>{repr(error)}</h2><a href='/'>back</a>"
    else:
        print('Nay')
        return redirect('/')


@app.route('/signup', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            res = request.form.to_dict()
            if res['username'] == '':
                raise Exception('username cannot be empty')
            if session.query(User).filter(
                    User.username == res['username']).first():
                raise Exception('Username already exists')

            if res['password'] != res['repeat']:
                raise Exception('Password and repeat password don\'t match')

            hashed = bcrypt.hashpw(
                res['password'].encode('utf8'), bcrypt.gensalt())
            newUser = User(username=res['username'],
                           password=hashed, login_count=1)
            session.add(newUser)
            session.commit()

            return f"<h2>Welcome to website {res['username']}<h2><a href='/'>back</a>"
        except Exception as error:
            return f"<h2>{repr(error)}</h2><a href='/'>back</a>"
    else:
        print('Nay')
        return redirect('/')
