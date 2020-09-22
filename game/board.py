import os
from random import choice

class Board:
    def __init__(self,):
        self._board = []
        self._len = 0
        self._size = 0

    def get_c(self, i):
        return self._board[i][0]

    @property
    def len(self):
        return self._len

    @property
    def size(self):
        return self._size

    def create_from_str(self, board_str):
        self._len = len(board_str)
        self._size = int(self._len ** 0.5)
        self._board = [0] * self._len

        for i in range(self._len):
            next_options = self._next_options(i)
            self._board[i] = (board_str[i], next_options)

    def load_from_file(self, path="board.txt"):
        file = open(path, "r")
        board = []
        while True:
            line = file.readline()
            # end of file
            if not line:
                break
            word = line.strip().lower()
            # empty sting
            if not word:
                continue
            board.append(word)
        file.close()
        self.create_from_str("".join(board))

    def next_options(self, cur):
        return self._board[cur][1]

    def _go_up(self, cur):
        if cur < self._size:
            return None
        return cur - self._size

    def _go_down(self, cur):
        # TODO cache (self._len - self._size)
        if cur >= (self._len - self._size):
            return None
        return cur + self._size

    def _go_right(self, cur):
        if (cur + 1) % self._size == 0:
            return None
        return cur + 1

    def _go_left(self, cur):
        if cur % self._size == 0:
            return None
        return cur - 1

    def _next_options(self, cur):
        options = []
        option = self._go_right(cur)
        if option is not None:
            options.append(option)
        option = self._go_left(cur)
        if option is not None:
            options.append(option)
        option = self._go_up(cur)
        if option is not None:
            options.append(option)
        option = self._go_down(cur)
        if option is not None:
            options.append(option)
        return options

    @staticmethod
    def generate_random(size=10, path="random_board.txt"):
        chars = "abcdefghijklmnopqrstuvwxyz"
        board = []

        for i in range(size):
            word = []
            for j in range(size):
                word.append(choice(chars))
            board.append("".join(word))

        with open(path, 'w') as file:
            file.write(os.linesep.join(board))
            file.close()


