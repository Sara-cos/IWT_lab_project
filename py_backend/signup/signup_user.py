from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv
import config


class Registration:

    def __init__(self, record, message=None):
        try:
            load_dotenv("py_backend/env/email_credentials.env")
            self.sender_email = os.getenv("EMAIL")
            self.sender_password = os.getenv("PASSWORD")
            self.user_data = {
                "firstname": record["First Name"],
                "lastname": record["Last Name"],
                "email": record["Email"],
                "phone": int(record["Phone Number"]),
                "password": generate_password_hash(record["Password"]),
                "gender": record["gender"]
            }
        except Exception as e:
            config.logger.log("ERROR", str(e))

    def insert_to_db(self):
        try:
            check_existence = config.mongo_db.my_db['User'].find({"email": self.user_data['email']})
            if len(list(check_existence)) == 0:
                res = config.mongo_db.insert_one("users", self.user_data)
                return res
            else:
                return {"status": False, "message": "User already exists"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}
