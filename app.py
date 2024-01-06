from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import random

application = Flask(__name__)
application.config["SECRET_KEY"] = "wodjsl"

DB = DBhandler()

# 메인
@application.route('/')
def hello():
    return render_template('index.html')

# 로그인
@application.route("/login")
def login():
    return render_template("login.html")

# 로그인 입력 정보 넘겨주기
@application.route("/login_confirm", methods=['POST'])
def login_user():
    id = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id, pw_hash):
        session['id'] = id
        return redirect(url_for('hello'))
    else:
        flash("아이디 혹은 비밀번호가 틀렸습니다.")
        return render_template("login.html")

# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

# 회원가입
@application.route("/signup")
def signup():
    return render_template("signup.html")

# 회원가입 입력 정보 넘겨주기
@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("이미 존재하는 아이디입니다.")
        return render_template("signup.html")

# 문제 추가 페이지
@application.route("/add_quiz")
def add_quiz():
    return render_template("add_quiz.html")

# 맞은 문제 추가 정보 넘기기
@application.route("/add_correct_result", methods=['POST'])
def add_correct_result():
    add = set(request.form['add_correct_num'].split())
    correct = str(DB.get_correct(session['id']))
    if correct:
        correct = set(correct.split())
    else:
        correct = set({})
    wrong = str(DB.get_wrong(session['id']))
    if wrong:
        wrong = set(wrong.split())
    else:
        wrong = set({})
    correct = correct.union(add)
    wrong = wrong.difference(correct)
    new_correct = " ".join(correct)
    new_wrong = " ".join(wrong)
    DB.init_quiz(session['id'], new_correct, new_wrong)
    return redirect(url_for('add_quiz'))

# 틀린 문제 추가 정보 넘기기
@application.route("/add_wrong_result", methods=['POST'])
def add_wrong_result():
    add = set(request.form['add_wrong_num'].split())
    correct = str(DB.get_correct(session['id']))
    if correct:
        correct = set(correct.split())
    else:
        correct = set({})
    wrong = str(DB.get_wrong(session['id']))
    if wrong:
        wrong = set(wrong.split())
    else:
        wrong = set({})
    wrong = wrong.union(add)
    correct = correct.difference(wrong)
    new_correct = " ".join(correct)
    new_wrong = " ".join(wrong)
    DB.init_quiz(session['id'], new_correct, new_wrong)
    return redirect(url_for('add_quiz'))

# 맞은 문제 초기화 정보 넘기기
@application.route("/init_correct_result", methods=['POST'])
def init_correct_result():
    correct = set(request.form['correct_numbers'].split())
    data = str(DB.get_wrong(session['id']))
    if data:
        wrong = set(data.split())
    else:
        wrong = set({})
    wrong = wrong.difference(correct)
    new_correct = " ".join(correct)
    new_wrong = " ".join(wrong)
    DB.init_quiz(session['id'], new_correct, new_wrong)
    return redirect(url_for('add_quiz'))

# 틀린 문제 초기화 정보 넘기기
@application.route("/init_wrong_result", methods=['POST'])
def init_wrong_result():
    wrong = set(request.form['wrong_numbers'].split())
    data = str(DB.get_correct(session['id']))
    if data:
        correct = set(data.split())
    else:
        correct = set({})
    correct = correct.difference(wrong)
    new_correct = " ".join(correct)
    new_wrong = " ".join(wrong)
    DB.init_quiz(session['id'], new_correct, new_wrong)
    return redirect(url_for('add_quiz'))

# 문제 뽑기 페이지
@application.route('/result', methods=['POST'])
def result():
    correct_numbers = request.form['correct_numbers']
    correct_numbers_list = [int(num) for num in correct_numbers.split()]

    wrong_numbers = request.form['wrong_numbers']
    wrong_numbers_list = [int(num) for num in wrong_numbers.split()]

    total_numbers_list = wrong_numbers_list + correct_numbers_list

    if not correct_numbers_list:
        return "맞은 문제 번호를 입력하세요."
    
    if not wrong_numbers_list:
        return "틀린 문제 번호를 입력하세요."

    selected_correct_number = random.choice(correct_numbers_list)
    selected_wrong_number = random.choice(wrong_numbers_list)
    selected_total_number = random.choice(total_numbers_list)
    return render_template('result.html', selected_correctNumber=selected_correct_number, selected_wrongNumber=selected_wrong_number, selected_total_number=selected_total_number)

if __name__ == '__main__':
    application.run(debug=True)
