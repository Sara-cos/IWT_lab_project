import config
from werkzeug.security import check_password_hash


class MyWall:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_password_and_retrieve(self):
        try:
            if self.email is not None and self.password is not None:
                self.email = self.email.lower()
                result = config.mongo_db.my_db['users'].find({"email": self.email})[0]
                if result is None:
                    config.logger.log("CRITICAL", "Invalid Credentials")
                    return {"status": False, "message": "Invalid Credentials"}
                else:
                    if check_password_hash(result['password'], self.password):
                        info = {
                            "firstname": result["firstname"],
                            "lastname": result["lastname"],
                            "email": result["email"],
                            "phone": result["phone"],
                            "gender": result["gender"]
                        }
                        return {"status": True, "message": info}
                    else:
                        config.logger.log("WARNING", "Wrong password...")
                        return {"status": False, "message": "Wrong password"}
            else:
                return {"status": False, "message": "Please enter an email and password"}
        except Exception as e:
            config.logger.log("ERROR", str(e))
            return {"status": False, "message": "Internal Server Error"}

    def check_password_and_change_information(self, record):
        try:
            condition = {"email": self.email}
            new_val = {
                "$set": {
                    "email": record["email"],
                    "firstname": record["firstname"],
                    "lastname": record["lastname"],
                    "gender": record["gender"],
                    "phone": record["phone"]
                }
            }
            res = config.mongo_db.my_db.update("users", condition, new_val)
            return res
        except Exception as e:
            return {"status": False, "message": "Internal server error"}

