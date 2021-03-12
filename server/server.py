from flask import Flask, request, Response
import sudoku
import generator


app = Flask(__name__)


@app.route("/solve", methods=["POST"])
def solve():
    payload = request.get_json()

    if (not payload) or ("board" not in payload):
        return Response("You must provide sudoku board in request", 400)

    board_in_string = payload["board"]
    board = sudoku.string_to_board(board_in_string)

    response = {
        "valid": False,
        "input_board": board_in_string,
        "output_board": board_in_string,
    }

    if sudoku.solve(board, 0, 0):
        response["output_board"] = sudoku.board_to_string(board)
        response["valid"] = True

    return response


@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json()

    if (not payload) or ("difficulty" not in payload):
        return Response("You must provide difficulty in request", 400)

    difficulty = payload["difficulty"]

    if difficulty not in ("easy", "hard"):
        return Response("Difficulty must be easy or hard", 400)

    board = generator.generate(difficulty)

    response = {
        "difficulty": difficulty,
        "board": board,
    }

    return response


if __name__ == "__main__":
    app.run(debug=True)
