import pygame
import time
import sudoku_game

pygame.font.init()


class Grid:
    """
    This class is all about developing the UI of the
    Sudoku game and updating the board and giving
    solved sudoku when asked
    """

    board = sudoku_game.generate("easy")

    def __init__(self, rows, cols, width, height, win):
        """This function initializes all the required parameters
        for the sudoku game

        params : rows [int], cols [int], width [int], height [int], win [int]
        """
        self.rows = rows
        self.cols = cols
        self.cubes = [
            [Cube(self.board[i][j], i, j, width, height) for j in range(cols)]
            for i in range(rows)
        ]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        """Update values of all cubes"""

        self.model = [
            [self.cubes[i][j].value for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def place(self, val):
        """Updates the value of particular cell

        params : val : int
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        """Displays temporary value entered by the user on cell

        params : val : int
        """
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        """Draws entire board with grid lines and cell values"""

        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(
                self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick
            )
            pygame.draw.line(
                self.win,
                (0, 0, 0),
                (i * gap, 0),
                (i * gap, self.height),
                thick,
            )

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        """Marks the current selected cell by user"""
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        """Clears the selected cell's temporary value"""
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        param : pos

        return : (row, col) on the board
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        """
        This function check whether the user has filled all the
        blank cubes or not.

        returns : boolean value
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def update_grid(self, new_board):
        """
        This function updates the values of
        the entire board

        params : new_board [list]
        """
        for row in range(9):
            for col in range(9):
                self.model[row][col] = new_board[row][col]
                self.cubes[row][col].set(new_board[row][col])
                self.cubes[row][col].draw_change(self.win, True)
                self.board[row][col] = new_board[row][col]
                self.update_model()
                pygame.display.update()
                pygame.time.delay(5)


class Cube:
    """
    This class is all about developing different 81 cubes of
    sudoku game.
    """

    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        """Initializes the cube"""
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """
        This function draws the cubes in the given space.

        params : win (the space of the entire board) [list]
        """
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(
                text,
                (
                    x + (gap / 2 - text.get_width() / 2),
                    y + (gap / 2 - text.get_height() / 2),
                ),
            )

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, by_user=True):
        """Draws changed value of the cell

        params : win : window

        by_user : boolean (False : value entered by user)
        """
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(
            text,
            (
                x + (gap / 2 - text.get_width() / 2),
                y + (gap / 2 - text.get_height() / 2),
            ),
        )
        if by_user:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        """Sets the real value of cube

        params : val : int
        """
        self.value = val
        self.temp = 0

    def set_temp(self, val):
        """Sets the temporary value of cube

        params : val : int
        """
        self.temp = val


def find_empty(board):
    """Finds empty cell

    params : board : list (sudoku 9x9 board)
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(board, val, pos):
    """Checks if value is valid to be entered in the cell or not

    params : val : int

    pos : tuple (cell cordinates)

    returns : boolean
    """

    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == val and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == val and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == val and (i, j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes):
    """
    This function draws various buttons, and displays time on
    the sudoku window

    params : win : window

    board : list (9x9 grid)

    time : time elapsed

    strikes : int (1:)
    """
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (210, 255, 255), (0, 0, 560, 540), 0)
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render(format_time(time), 1, (0, 0, 0))
    win.blit(text, (375, 563))

    # Draw Easy Button
    text = fnt.render("Easy", 1, (0, 0, 0))
    pygame.draw.rect(win, (150, 150, 0), [20, 560, 80, 33], 0)
    win.blit(text, (30, 565))

    # Draw border for Easy Button
    pygame.draw.rect(win, (0, 0, 0), [20, 560, 80, 33], 4)

    # Draw Hard Button
    text = fnt.render("Hard", 1, (0, 0, 0))
    pygame.draw.rect(win, (150, 0, 0), [120, 560, 80, 33], 0)
    win.blit(text, (130, 565))

    # Draw border for Hard Button
    pygame.draw.rect(win, (0, 0, 0), [120, 560, 80, 33], 4)

    # Draw Solve Button
    text = fnt.render("Solve", 1, (0, 0, 0))
    pygame.draw.rect(win, (0, 150, 0), [220, 560, 90, 33], 0)
    win.blit(text, (230, 565))

    # Draw border for Solve Button
    pygame.draw.rect(win, (0, 0, 0), [220, 560, 90, 33], 4)

    # Draw Strikes
    if strikes == 1:
        img = pygame.image.load("images/red_cross.png")
        img = pygame.transform.scale(img, (40, 40))
        win.blit(img, (330, 555))
    elif strikes == 2:
        img = pygame.image.load("images/green_tick.jpg")
        img = pygame.transform.scale(img, (40, 40))
        win.blit(img, (330, 555))

    # Draw grid and board
    board.draw()


def format_time(secs):
    """
    This function is all about displaying time on the window.

    params : sec [int]

    returns : string
    """
    if type(secs) == str:
        return secs
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = "Time: " + str(hour) + ":" + str(minute) + ":" + str(sec)
    return mat


def main():
    """Draws main window and handle events generated
    from user interactions
    """
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:
        if start != "stop":
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                            strikes = 2
                        else:
                            print("Wrong")
                            strikes = 1
                        key = None

                        if board.is_finished():
                            strikes = 0
                            print("Game over")
                            play_time = "You won!!!"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                # Easy Button Clicked
                if 20 <= pos[0] <= 100 and 560 <= pos[1] <= 560 + 33:
                    new_board = sudoku_game.generate("easy")
                    board.update_grid(new_board)
                    start = time.time()
                    strikes = 0

                # Hard Button Clicked
                elif 120 <= pos[0] <= 200 and 560 <= pos[1] <= 560 + 33:
                    new_board = sudoku_game.generate("hard")
                    board.update_grid(new_board)
                    strikes = 0
                    start = time.time()

                # Solve Button Clicked
                elif 220 <= pos[0] <= 310 and 560 <= pos[1] <= 560 + 33:
                    solved_board = sudoku_game.solve(board.board)
                    board.update_grid(solved_board)
                    strikes = 0
                    play_time = "Solved!!!"
                    start = "stop"
                elif clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
