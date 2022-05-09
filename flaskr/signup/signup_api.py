from flaskr.signup.signup_user import Registration
from flask_restful import Resource
from flask import request
import config


class Signup(Resource):

    def post(self):
        try:
            config.logger.log("INFO", "Starting registration process...")
            record = request.get_json()
            return Registration(record).insert_to_db()
        except Exception as e:
            config.logger.log("ERROR", str(e))
