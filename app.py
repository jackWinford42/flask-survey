from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

RESPONSES_KEY = "responsesKey"
question = "question"

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

    return redirect("/questions/0")

@app.route('/questions/<int:integer>')
def show_question(integer):
    """Return a seprate rendered template for each question in the survey"""
    responses = session[RESPONSES_KEY]

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")

    if (len(responses) != integer):
        flash(f"Questions are being accessed out of order. Question id: {integer}")
        return redirect(f"/questions/{len(responses)}")

    current_question = satisfaction_survey.questions[integer]
    return render_template("question.html", question=current_question)

@app.route('/answer', methods=["POST"])
def handle_answer():
    """When an answer is submitted it is appended to the responses list, and
    the page is redirected to the next question"""
    other_num = session[question]
    other_num = other_num + 1
    session[question] = other_num

    answer = request.form['answer']
    
    #add answer to list of responces
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    return redirect(f"/questions/{other_num}")

@app.route('/complete')
def complete():
    """when the survey has been completed display a page thanking the user
    for comleting the survey"""
    return render_template("completed.html")