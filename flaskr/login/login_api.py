from flask import request
from flask_restful import Resource
from flaskr.login.login_user import Validation
import config


class Login(Resource):

    def post(self):
        try:
            config.logger.log("INFO", "Starting log in process...")
            email = request.get_json()['formData']['email']
            password = request.get_json()['formData']['password']
            role = request.get_json()['formData']['role']
            result = Validation(email, password, role).check()
            return result
        except Exception as e:
            config.logger.log("ERROR", str(e))
