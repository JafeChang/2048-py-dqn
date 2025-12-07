import numpy as np
import random

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.score = 0
        self._add_random_tile()
        self._add_random_tile()

    def _add_random_tile(self):
        empties = list(zip(*np.where(self.board == 0)))
        if not empties:
            return
        y, x = random.choice(empties)
        self.board[y, x] = 4 if random.random() < 0.1 else 2

    def clone(self):
        g = Game2048(self.size)
        g.board = self.board.copy()
        g.score = self.score
        return g

    def can_move(self):
        if np.any(self.board == 0):
            return True
        for y in range(self.size):
            for x in range(self.size - 1):
                if self.board[y, x] == self.board[y, x+1]:
                    return True
        for y in range(self.size - 1):
            for x in range(self.size):
                if self.board[y, x] == self.board[y+1, x]:
                    return True
        return False

    def move(self, direction):
        # direction: 'up','down','left','right'
        rotated = self._rotate_for_direction(direction)
        moved_board, gained = self._move_left(rotated)
        board_after = self._rotate_back(moved_board, direction)
        changed = not np.array_equal(self.board, board_after)
        self.board = board_after
        self.score += gained
        if changed:
            self._add_random_tile()
        return changed, gained

    def _rotate_for_direction(self, direction):
        b = self.board.copy()
        if direction == 'up':
            return np.rot90(b, -1)
        if direction == 'right':
            return np.rot90(b, 2)
        if direction == 'down':
            return np.rot90(b, 1)
        return b

    def _rotate_back(self, board, direction):
        if direction == 'up':
            return np.rot90(board, 1)
        if direction == 'right':
            return np.rot90(board, 2)
        if direction == 'down':
            return np.rot90(board, -1)
        return board

    def _move_left(self, board):
        gained = 0
        out = np.zeros_like(board)
        for i in range(self.size):
            row = board[i, :]
            tight = row[row != 0]
            new_row = []
            skip = False
            for j in range(len(tight)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(tight) and tight[j] == tight[j+1]:
                    new_row.append(tight[j]*2)
                    gained += tight[j]*2
                    skip = True
                else:
                    new_row.append(tight[j])
            new_row = np.array(new_row + [0]*(self.size - len(new_row)), dtype=int)
            out[i, :] = new_row
        return out, gained

    def to_list(self):
        return self.board.tolist()

    def is_game_over(self):
        return not self.can_move()
