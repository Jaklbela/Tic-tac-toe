from flask import Flask, request, abort, render_template
from collections import namedtuple

app = Flask(__name__)

Game = namedtuple('Game', ['board', 'next_turn', 'scores'])
games = {}


@app.route('/')
def home():
    return render_template('web.html')


@app.route('/new_game', methods=['POST'])
def new_game():
    game_id = str(len(games) + 1)
    games[game_id] = Game(board=[None] * 9, next_turn='X', scores={'X': 0, 'O': 0})
    return game_id


@app.route('/make_move', methods=['POST'])
def make_move():
    game_id = request.json['game_id']
    player = request.json['player']
    position = request.json['position']

    if game_id not in games:
        abort(404)

    game = games[game_id]

    if game.board[position] is not None:
        abort(400, 'Invalid move')

    if game.next_turn != player:
        abort(400, 'Not your turn')

    board = game.board[:]
    board[position] = player
    next_turn = 'O' if player == 'X' else 'X'
    scores = game.scores.copy()

    if check_win(board, position):
        scores[player] += 1
        board = [None] * 9

    games[game_id] = Game(board=board, next_turn=next_turn, scores=scores)

    return {'board': board, 'next_turn': next_turn, 'scores': scores}


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


if __name__ == '__main__':
    app.run(debug=True)
