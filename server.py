import time
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from redis import Redis
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

redis = Redis()


@app.route('/')
def draw():
    if "board" not in session:
        session["board"] = [None] * 9
        session["turn"] = 'X'
        session["scores"] = {'X': 0, 'O': 0}

    session['last_seen'] = time.time()

    return render_template("web.html", game=session["board"], turn=session["turn"], score=session["scores"])


@app.route('/make_move/<int:index>')
def make_move(index):
    session["board"][index] = session["turn"]

    if check_win(session["board"], index):
        session["scores"][session["turn"]] += 1
        session["board"] = [None] * 9
    else:
        if session["turn"] == 'X':
            session["turn"] = 'O'
        else:
            session["turn"] = 'X'

    return redirect(url_for("draw"))


@app.route('/new_game')
def new_game():
    session["board"] = [None] * 9
    session["turn"] = 'X'
    session["scores"] = {'X': 0, 'O': 0}

    return redirect(url_for("draw"))


def check_win(board, last_move):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
        [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
    ]

    player = board[last_move]

    for combination in winning_combinations:
        if all(map(lambda pos: board[pos] == player, combination)):
            return True
    return False


@app.before_request
def check_timeout():
    last_seen = session.get('last_seen')
    if last_seen and time.time() - last_seen > 30:
        session.clear()


if __name__ == '__main__':
    app.run(debug=True)
