from bson.objectid import ObjectId
from flask_restful import Resource
from flask import request
import config

class user_profile(Resource):
    def post(self):
        pass



#DB.collection.find_one({'_id': ObjectId(post_id)})