import config
from uuid import uuid1


class Question:

    def insert_a_question(self, record):
        data = dict(
            question_id = str(uuid1()),
            question = record["Question"],
            option1 = record["Option-1"],
            option2 = record["Option-2"],
            option3 = record["Option-3"],
            option4 = record["Option-4"],
            answer = int(record["Correct Option"]),
            exam_id = record["Exam ID"]
        )
        config.mongo_db.insert_one("questions", data)

    def get_all_questions(self, exam_id):
        result = config.mongo_db.my_db['questions'].find({"exam_id": exam_id})
        return result

    

