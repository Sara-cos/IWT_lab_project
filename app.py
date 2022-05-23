from flask import Flask, render_template, request, redirect, session, url_for
from py_backend.logger.log_db import Logger
from py_backend.mongo_db.crud import Operations
from py_backend.signup.signup_user import Registration
from py_backend.login.login_user import Validation
import config
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
config.logger = Logger()
config.mongo_db = Operations("ExamPortal", config.logger)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('Home.html')


@app.route('/auth/login', methods=['GET', 'POST'])
def login_page():
    if not session.get('email'):
        return render_template('login.html')
    return redirect('/auth/user')


@app.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    session["email"] = None
    session['password'] = None
    return redirect('/')


@app.route('/auth/login-user', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["Email"]
        password = request.form["Password"]
        res = Validation(email, password).check()
        if res["status"]:
            session["email"] = email
            session["password"] = password
            return redirect('/auth/user')
        return res


@app.route('/auth/user', methods=["GET", "POST"])
def show_user():
    return session.get("email")


@app.route('/auth/signup', methods=['GET', 'POST'])
def signup_page():
    return render_template('Registration.html')


@app.route('/auth/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        record = request.form
        password = request.form["Password"]
        confirm_password = request.form["Confirm Password"]
        if password == confirm_password:
            res = Registration(record).insert_to_db()
            return res
        else:
            return {"status": False, "message": "Password does not match"}


if __name__ == '__main__':
    config.logger.log("INFO", "App starting")
    app.run(debug=True)
