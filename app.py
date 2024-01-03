from flask import Flask, render_template, request
import random

app = Flask(__name__)

# 메인
@app.route('/')
def index():
    return render_template('index.html')

# 문제 뽑기 페이지
@app.route('/result', methods=['POST'])
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
    app.run(debug=True)
