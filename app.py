from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

RESPONSES_KEY = "responsesKey"
question = "question"


app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

""" RESPONSES_KEY = "responsesKey"
question = 0 """

@app.route('/')
def start_page():
    """Display the home/start page of the survey app"""

    return render_template("start.html", survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def begin_survey():
    session[RESPONSES_KEY] = []
    session[question] = 0

    #number = session[question]
    return redirect("/questions/0")

@app.route(f'/questions/{session[question]}')
def show_question(qid):
    """Return a seprate rendered template for each question in the survey"""
    current_question = satisfaction_survey.questions[session[question]]
    return render_template("question.html", question=current_question)

@app.route('/answer', methods=["POST"])
def handle_answer():
    """When an answer is submitted it is appended to the responses list, and
    the page is redirected to the next question"""
    other_num = session[question]
    other_num = other_num + 1
    session[question] = other_num

    answer = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    #string = "/questions/" + other_num

    return redirect(f"/questions/{other_num}")
