from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://test0:test@cluster0.bbyas.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def hello():
    return "hello :)"


if __name__ == "__main__":
    app.run(debug=True)


