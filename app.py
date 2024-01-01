from flask import Flask, render_template
import sys
application = Flask(__name__)

# 메인
@application.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)