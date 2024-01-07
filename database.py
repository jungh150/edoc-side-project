import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    # 회원가입
    def insert_user(self, data, pw):
        user_info = {
            "pw": pw
        }
        quiz_numbers = {
            "correct" : "",
            "wrong" : ""
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("users").child(data['id']).child("user_info").set(user_info)
            self.db.child("users").child(data['id']).child("quiz_numbers").set(quiz_numbers)
            return True
        else:
            return False

    # 회원가입 시 중복 체크
    def user_duplicate_check(self, id_string):
        users = self.db.child("users").get()
        if str(users.val()) == "None":  # 첫 회원가입
            return True
        else:
            if id_string in users.val():
                return False
        return True

    # 로그인
    def find_user(self, id, pw):
        users = self.db.child("users").get()
        for user in users.each():
            user_id = user.key()
            if user_id == id:
                user_data = user.val()
                user_info = user_data.get("user_info")
                if user_info.get("pw") == pw:
                    return True
                else:
                    return False
        return False
    
    # 맞은 문제 가져오기
    def get_correct(self, id) :
        data = self.db.child("users").child(id).child("quiz_numbers").get().val().get('correct')
        return data

    # 틀린 문제 가져오기
    def get_wrong(self, id) :
        data = self.db.child("users").child(id).child("quiz_numbers").get().val().get('wrong')
        return data

    # 문제 초기화
    def init_quiz(self, id, correct, wrong):
        if correct == "None":
            correct =  ""
        if wrong == "None":
            wrong =  ""
        quiz_numbers = {
            "correct" : correct, 
            "wrong" : wrong
        }
        self.db.child("users").child(id).child("quiz_numbers").set(quiz_numbers)
        return True