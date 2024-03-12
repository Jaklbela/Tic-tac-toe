const gameBoard = document.querySelector('#gameBoard');

let player = 'X'
let gameId = null;

function newGame() {
    fetch('http://127.0.0.1:5000/new_game', {
        method: 'POST'
    }).then(response => response.text())
    .then(id => {
        gameId = id;
        gameBoard.innerHTML = '<div class="cell" onclick="makeMove(0)"></div>' +
                              '<div class="cell" onclick="makeMove(1)"></div>' +
                              '<div class="cell" onclick="makeMove(2)"></div>' +
                              '<div class="cell" onclick="makeMove(3)"></div>' +
                              '<div class="cell" onclick="makeMove(4)"></div>' +
                              '<div class="cell" onclick="makeMove(5)"></div>' +
                              '<div class="cell" onclick="makeMove(6)"></div>' +
                              '<div class="cell" onclick="makeMove(7)"></div>' +
                              '<div class="cell" onclick="makeMove(8)"></div>';
    });
}

function makeMove(index) {
    if (!gameId) {
        return;
    }

    fetch('http://127.0.0.1:5000/make_move', {
        method: 'POST',
        body: JSON.stringify({
            game_id: gameId,
            player: 'X',
            position: index
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(result => {
        if (result.winner) {
            alert(result.winner + ' wins!');
        }
        document.querySelectorAll('.cell')[index].innerText = player;
    });
}

function updateBoard() {
    fetch('http://127.0.0.1:5000/get_board', {
        method: 'POST',
        body: JSON.stringify({
            game_id: gameId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(board => {
        board.forEach((cell, index) => {
            gameBoard.children[index].textContent = cell;
        });
    });
}

newGame();
