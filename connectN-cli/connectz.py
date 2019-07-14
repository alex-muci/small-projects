"""
NB: only standard Python 3.6 libraries allowed
(numpy would make winning checks faster)
"""
import sys
# import argparse
# from typing import List


def CODE_OUTPUT(out): print(out); return  # sys.exit()

def is_straight(_s): return 0 not in _s and len(_s) == 1


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                  ConnectZ game
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ConnectZ:
    """
    Generalization of the classical Connect 4 game using only standard Python 3.6 libraries.

    Class built to be called from this script by running:
        python connectz.py [inputfilename]

        [inputfilename] is an ASCII textfile with the following features:
        - the first line contains three integers, respectively, the (i) no of columns and (ii) rows of the board/frame
        and the (iii) minimum number of pieces/counters required to win a game.
        - each subsequent line is a single integer representing a move in the game (column where piece drops),
        starting with player one and alternating.

    Customisations:
    - board dimensions (rows X cols) and
    - no. of adjacent pieces to win.

    Two versions available for checking wins: fast provides speedup for larger dimensions.
    Most efficient would be to rewrite it in numpy and numba but implementation restricted to standard libraries only.
    """

    def __init__(self, cols_width=7, rows_height=6, win_moves_n=4, fast_version=True):
        """
        :param cols_width: width of the frame in columns.
        :param rows_height: height of the frame in rows.
        :param win_moves_n: minimum number of straight pieces/counters to win the game.
        :param fast_version: If true, use fast version rather than the slow/naive one.

        default params are the classical Connect 4 (and fast check-wins version).
        """
        self.cols = cols_width
        self.rows = rows_height
        self.n = win_moves_n

        # ERROR Code 7: Illegal game
        if self.n > max(self.rows, self.cols):
            CODE_OUTPUT(7)

        # ERROR Code 3: Incomplete game  ("Note that a file with only a dimensions line constitutes an incomplete game")
        if self.cols == 1 or self.rows == 1 or self.n == 1:
            CODE_OUTPUT(3)

        # list of list (more efficient with numpy.array but not allowed here)
        self.board = [[0]*self.cols for _ in range(self.rows)]

        # fast version (dynamically assigned)
        self.fast_version = fast_version
        self.c, self.r = None, None    # current column and row in run()
        self.check_win = self.check_win_fast if self.fast_version else self.check_win_slow

    def check_valid_move(self, col_j):
        """
        Is the selected column legal?
         - col_j must be inside the board ("legal column") and
         - not already full ("legal row" - by checking top row: self.board[0])
        """
        # ERROR Code 6: Illegal column - (file OK, but column outside board)
        if col_j > self.cols or col_j < 1:
            CODE_OUTPUT(6)

        # ERROR Code 5: Illegal row - (column legal, but column already full)
        elif self.board[0][col_j-1] != 0:
            CODE_OUTPUT(5)

    def place_piece(self, player, col_j):
        """
        Place the player piece in the first empty row of col_j (board position).
        (0 is replaced by the player no., either 1 or 2, starting from the board bottom).
        """
        # column position for the board, e.g. [0, cols_width-1]
        board_col = col_j - 1

        for j, row in enumerate(reversed(self.board)):   # self.board[::-1]:  #  shallow copy, hence assignment below
            if row[board_col] == 0:
                row[board_col] = player
                # for check_win_fast: keep track of current row and column
                self.r, self.c = self.rows-j-1, board_col  # NB: bottom row is self.rows-1, top row is 0
                return

    def check_win_slow(self, player):
        """
        brute-force check of all self.n combinations, every time
        """
        # all horizontal checks
        for row in reversed(self.board):
            for c in range(self.cols - self.n + 1):
                if 0 not in row[c:c+self.n] and len(set(row[c:c+self.n])) == 1:  # and sum(row[c:c+self.n])==self.n*player
                    return True

        # all vertical checks
        for col in zip(*self.board):  # tuple
            for r in range(self.rows - self.n + 1):
                if 0 not in col[r:r + self.n] and len(set(col[r:r + self.n])) == 1:
                    return True

        # all right diagonals checks
        for c in range(self.cols - self.n + 1):
            for r in range(self.rows - self.n + 1):
                if all(self.board[r+a][c+a] == player for a in range(self.n)):
                    return True

        # all left diagonal checks
        for c in range(self.cols - self.n + 1):
                if any(all(self.board[r-a][c+a] == player for a in range(self.n)) for r in range(self.n, self.rows)):
                    return True

    def check_win_fast(self, player):
        """
        faster version checking only around current piece
        (which avoiding unnecessary rows/cols nested-loop checks)

        """
        # TODO: further optimisation, and test meimozation vs. all combo in dict at start (faster, but + memory)

        # auxiliary variables
        left = self.c + 1 - self.n; left_max = self.cols - self.n + 1   # horizional
        down  = self.r + self.n                                         # vertical

        diagP_down = min(self.n-1, self.c, self.rows-1 - self.r)        # diagonals...
        diagN_down = min(self.n-1, self.cols-1 - self.c, self.rows-1 - self.r)

        diagP_up   = min(self.n-1, self.cols-1 - self.c, self.r)
        diagN_up   = min(self.n-1, self.c, self.r)

        diagP_loop = max(0, diagP_down + diagP_up - 1)
        diagN_loop = max(0, diagN_down + diagN_up - 1)

        # 1. horizontals (1 row)
        for col in range(max(left, 0), min(left_max, self.c+1)):
            cells = set(self.board[self.r][col:col + self.n])
            if is_straight(cells): return True

        # 2. vertical down (#1 check)
        if down <= self.rows:
            cells = set(list(zip(*self.board))[self.c][self.r:down])
            if is_straight(cells): return True

        # 3. positive-sloped diagonals (#1 loop: from bottom to up right)
        _1row, _1col = self.r + diagP_down, self.c - diagP_down
        for x in range(diagP_loop):  # if range(negative or zero) no loop
            cells = set([self.board[_1row-x-a][_1col+x+a] for a in range(self.n)])
            if is_straight(cells): return True

        # 4. negative-sloped diagonals (#1 loop: from bottom to up left)
        _1row, _1col = self.r + diagN_down, self.c + diagN_down
        for x in range(diagN_loop):  # if range(negative or zero) no loop
            cells = set([self.board[_1row - x - a][_1col - x - a] for a in range(self.n)])
            if is_straight(cells): return True

    def run(self, moves_list):

        player = 1  # player 1 always starts

        for i, col_j_ in enumerate(moves_list):

            self.check_valid_move(col_j_)
            self.place_piece(player, col_j_)

            # check if player won (TODO: insert min number of moves?)
            if self.check_win(player):

                #  ERROR Code 4: Illegal continue (game won but still playing on)
                if len(moves_list[i:]) > 1:
                    CODE_OUTPUT(4)
                #  player won (and no more moves)
                else:
                    CODE_OUTPUT(player)

            # switch player (inline if ... else)
            player = 2 if player == 1 else 1
            # player = 2 if (player % 2) else 1  # odd = 1, even = 2

        # DRAW: no wins and board full
        if not any(0 in row for row in self.board):
            CODE_OUTPUT(0)
        # INCOMPLETE: no wins, all moves completed (no pieces left) yet board NOT full
        else:
            CODE_OUTPUT(3)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':

    try:
        script, input_file = sys.argv
    except:  # ValueError:
        CODE_OUTPUT("connectz.py: Provide one input file"); sys.exit()

    try:
        with open(input_file, 'r') as in_file:
            lines = in_file.readlines()
    except:
        # ERROR Code 9: File error
        CODE_OUTPUT(9); sys.exit()

    try:
        width, height, win_moves = list(map(int, lines[0].rstrip().split()))
        moves = list(map(int, lines[1:]))
    except:
        # ERROR Code 8: Invalid file
        CODE_OUTPUT(8); sys.exit()

    game = ConnectZ(width, height, win_moves)

    game.run(moves)
