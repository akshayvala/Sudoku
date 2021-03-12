import sudoku
import random


def get_complete_sudoku(board, row, col):
    """Generates valid sudoku with random entries

    params : board : list (sudoku 9x9 grid)

    : row : int

    : col : int
    """

    if row == 8 and col == 8:
        valid_entries = sudoku.get_valid_entries(board, row, col)
        if len(valid_entries) == 0:
            return False
        board[row][col] = valid_entries[0]
        return True

    if col == 9:
        row = row + 1
        col = 0

    valid_entries = sudoku.get_valid_entries(board, row, col)
    if len(valid_entries) == 0:
        return False

    random.shuffle(valid_entries)

    # Fill Sudoku
    for entry in valid_entries:
        board[row][col] = entry
        if get_complete_sudoku(board, row, col + 1):
            return True
    board[row][col] = 0
    return False


def remove_some_entries(board, difficulty):
    """Removes some entries from sudoku based on difficulty

    board : list (sudoku 9x9 grid)

    : difficulty : string ("easy" or "hard")
    """
    indices = list(range(81))
    random.shuffle(indices)

    while indices:
        row = indices[0] // 9
        col = indices[0] % 9
        temp = board[row][col]
        board[row][col] = 0
        indices = indices[1:]

        copy_of_board = [row[:] for row in board]

        sudoku.fill_rigid_cell(copy_of_board)

        for line in copy_of_board:
            if 0 in line:
                num_solutions = sudoku.get_no_of_solution(copy_of_board, 0, 0)

                if num_solutions > 1:
                    board[row][col] = temp
                    if difficulty == "easy":
                        return
                break


def generate(difficulty):
    """Generates sudoku based on difficulty

    params : difficulty : str ("easy" / "hard")
    """
    difficulty.lower()
    board = [[0] * 9 for _ in range(9)]
    get_complete_sudoku(board, 0, 0)
    remove_some_entries(board, difficulty)
    return sudoku.board_to_string(board)
