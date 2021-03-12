def print_sudoku(board):
    """Prints sudoku at CLI

    params : board : list (sudoku 9x9 )
    """
    for row in range(9):
        for col in range(9):
            print(board[row][col], end=" ")
            if col + 1 == 3 or col + 1 == 6:
                print(" | ", end=" ")
        if row + 1 == 3 or row + 1 == 6:
            print("\n" + "-" * 25, end=" ")
        print()
    print()


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


def get_valid_entries(board, row, col):
    """Checks valid entries for given cell in sudoku

    params : board : list (sudoku 9 X 9)

    : row : int

    : col : int

    returns : list (list of valid entries)
    """
    used_entries = [0] * 10
    used_entries[0] = 1

    block_row = row // 3
    block_col = col // 3

    # Row and Column
    for m in range(9):
        used_entries[board[m][col]] = 1
        used_entries[board[row][m]] = 1

    # Square
    for m in range(3):
        for n in range(3):
            used_entries[board[m + block_row * 3][n + block_col * 3]] = 1

    valid_entries = [i for i in range(1, 10) if used_entries[i] == 0]
    return valid_entries


def get_no_of_solution(board, row, col):
    """Calulates no of valid solution for sudoku

    params : board : list (sudoku 9x9 grid)

    : row : int

    : col : int
    """
    no_of_solutions = 0

    if row == 8 and col == 8:
        if board[row][col] != 0:
            return 1
        else:
            valid_entries = get_valid_entries(board, row, col)
            return len(valid_entries)

    if col == 9:
        row = row + 1
        col = 0

    if board[row][col] == 0:

        valid_entries = get_valid_entries(board, row, col)

        if len(valid_entries) == 0:
            return 0

        while len(valid_entries) != 0:
            board[row][col] = valid_entries[0]
            valid_entries.remove(valid_entries[0])
            no_of_solutions += get_no_of_solution(board, row, col + 1)

        board[row][col] = 0
        return no_of_solutions
    else:
        no_of_solutions += get_no_of_solution(board, row, col + 1)
    return no_of_solutions


def fill_rigid_cell(board):
    """Fills cell which can have only one possible value in sudoku

    params : board : list (sudoku 9x9 grid)
    """
    filled = False

    while not filled:
        filled = True

        for row in range(9):
            for col in range(9):

                if board[row][col] != 0:
                    continue

                valid_entries = get_valid_entries(board, row, col)
                if len(valid_entries) == 1:
                    board[row][col] = valid_entries[0]
                    filled = False


def solve(board, row, col):
    """Solves sudoku using DFS with backtracking

    params : board : list (sudo 9x9 grid)

    : row : int

    : col : int
    """
    if row == 8 and col == 8:
        valid_entries = get_valid_entries(board, row, col)
        if len(valid_entries) != 0:
            board[row][col] = valid_entries[0]
        return True

    if col == 9:
        row = row + 1
        col = 0

    if board[row][col] == 0:
        valid_entries = get_valid_entries(board, row, col)
        for entry in valid_entries:
            board[row][col] = entry
            if solve(board, row, col + 1):
                return True

        # Ans not found
        board[row][col] = 0
        return False

    return solve(board, row, col + 1)
