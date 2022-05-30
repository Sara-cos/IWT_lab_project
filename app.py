from flask import Flask, render_template, request, redirect, session, url_for, send_file, send_from_directory
from py_backend.logger.log_db import Logger
from py_backend.mongo_db.crud import Operations
from py_backend.signup.signup_user import Registration
from py_backend.login.login_user import Validation
import config
import gridfs
from flask_session import Session
from py_backend.my_wall.display import MyWall
from py_backend.questions.questions import Question
from uuid import uuid1
import os


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
        return render_template("/auth/login", results=res["message"])


@app.route('/auth/user', methods=["GET", "POST"])
def show_user():
    email = session.get("email")
    password = session.get("password")
    res = MyWall(email, password).check_password_and_retrieve()
    if res["status"]:
        return render_template("Dashboard.html", **res["message"])
    else:
        return redirect("/auth/login")


@app.route('/auth/edit-user', methods=["GET", "POST"])
def edit_user():
    email = session.get("email")
    password = session.get("password")
    res = MyWall(email, password).check_password_and_retrieve()
    if res["status"]:
        return render_template("MyWalledit.html", **res["message"])
    else:
        return redirect("/auth/login")


@app.route('/auth/save-edit', methods=["GET", "POST"])
def save_edit():
    record = request.form
    email = session.get("email")
    password = session.get("password")
    res = MyWall(email, password).check_password_and_change_information(record)
    return redirect("/auth/user")


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
            return redirect('/auth/login')
        else:
            res = {"status": False, "message": "Password does not match"}
            return render_template("/auth/signup", results=res["message"])


@app.route("/question-page", methods=["GET", "POST"])
def question_page():
    return render_template("Qdemo.html")


@app.route("/set-question", methods=['GET', 'POST'])
def set_question():
    record = request.form
    Question().insert_a_question(record)
    return render_template("Qdemo.html")


@app.route("/set-exam-id", methods=['GET', 'POST'])
def set_exam_id():
    session["exam_id"] = request.form["exam_id"]
    session["question"] = 0


@app.route("/get-question", methods=['GET', 'POST'])
def get_question():
    # exam_id = request.form["exam_id"]
    exam_id = session['exam_id']
    question = Question().get_all_questions(exam_id)
    l = []
    for q in question:
        l.append(q)
    return l[session["question"]]


@app.route("/submit-exam", methods=["GET", "POST"])
def submit_exam():
    session["question"] = None
    session["score"] = None
    session["exam_id"] = None


@app.route("/repo-push", methods=["GET", "POST"])
def repo_push():
    fs = gridfs.GridFS(config.mongo_db.my_db)

    # define an image object with the location.
    file = "ZiClJf-1920w.jpg"

    # Open the image in read-only format.
    with open(file, 'rb') as f:
        contents = f.read()

    # Now store/put the image via GridFs object.
    fs.put(contents, filename=file, email=session["email"])
    return "True"


@app.route("/repo-show", methods=["GET", "POST"])
def repo_show():
    email = session["email"]
    files = []
    for file in config.mongo_db.my_db.fs.files.find({"email": email}):
        files.append(file["filename"])
    print(files)
    return str(files)


@app.route("/repo-download", methods=['GET', 'POST'])
def repo_download():
    # filename = request.form['filename']
    filename = "ZiClJf-1920w.jpg"
    email = session['email']
    fs = gridfs.GridFS(config.mongo_db.my_db)
    for grid_out in fs.find({"email": email, "filename": filename}):
        data = grid_out.read()
    path = os.path.join("tmp_files", filename)
    with open(path, "wb") as f:
        f.write(data)
    return send_file(path)


@app.route("/repo-delete", methods=["GET", "POST"])
def repo_delete():
    # filename = request.form['filename']
    filename = "ZiClJf-1920w.jpg"
    email = session['email']
    fs = gridfs.GridFS(config.mongo_db.my_db)
    for file in config.mongo_db.my_db.fs.files.find({"email": email, "filename": filename}):
        id = file["_id"]
    fs.delete(id)
    return "done"


if __name__ == '__main__':
    config.logger.log("INFO", "App starting")
    app.run(debug=True)
