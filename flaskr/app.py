from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
import config
import os
from flaskr.logger.log_db import Logger
from flaskr.mongo_db.crud import Operations
from flaskr.signup.signup_api import Signup
from flaskr.login.login_api import Login


app = Flask(__name__)
CORS(app)
config.logger = Logger()
config.mongo_db = Operations("DB", config.logger)
api = Api(app)

api.add_resource(Signup, '/api/signup')
api.add_resource(Login, '/api/login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)

