import requests
import json


SOLVE_ENDPOINT = "http://127.0.0.1:5000/solve"
GENERATE_ENDPOINT = "http://127.0.0.1:5000/generate"


def string_to_board(board_in_string):
    """Converts string into sudoku board

    params : board_in_string : string

    returns : list
    """
    board = []

    for row in range(9):
        row_list = []
        for col in range(9):
            row_list.append(int(board_in_string[row * 9 + col]))
        board.append(row_list)

    return board


def board_to_string(board):
    """Converts sudoku board from list to string

    params : board : list

    returns : string
    """
    board_in_string = ""

    for row in range(9):
        for col in range(9):
            board_in_string += str(board[row][col])

    return board_in_string


def solve(board):
    """Solves sudoku by making api call

    params : board : list (sudoku 9x9 grid)

    returns : solved_board : list (sudoku 9x9 grid)
    """
    board_in_string = board_to_string(board)
    payload = {"board": board_in_string}
    response = requests.post(
        SOLVE_ENDPOINT,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    ).json()
    solved_board = string_to_board(response["output_board"])
    return solved_board


def generate(difficulty):
    """Generates sudoku based on difficulty by making an api call

    params : difficulty : string ("easy" / "hard")

    returns : board : list (sudoku 9x9 grid)
    """
    payload = {"difficulty": difficulty}
    response = requests.post(
        GENERATE_ENDPOINT,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    ).json()
    board = string_to_board(response["board"])
    return board
