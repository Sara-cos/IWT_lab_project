import config
from uuid import uuid1


class Question:

    def insert_a_question(self, record):
        data = dict(
            question_id = str(uuid1()),
            question = record["question"],
            option1 = record["option1"],
            option2 = record["option2"],
            option3 = record["option3"],
            option4 = record["option4"],
            answer = record["answer"],
            exam_id = record["exam_id"]
        )
        config.mongo_db.insert_one("questions", data)

    def get_all_questions(self, exam_id):
        result = config.mongo_db.my_db['questions'].find({"exam_id": exam_id})
        return result

