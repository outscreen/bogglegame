from copy import copy
from datetime import datetime
from game.board import Board
from game.trie import Trie
from logger import logging

logger = logging.getLogger("start_game")


class Game:
    def __init__(self, board, trie, min_len=0, allow_repetitions=True):
        self.min_len = min_len
        self.allow_repetitions = allow_repetitions
        self.board = board
        self.trie = trie
        self.found = {}

    def dfs(self, trie, cur, visited, words, word_i):
        cur_c = self.board.get_c(cur)

        trie = trie.get(cur_c)
        if not trie:
            return

        visited[cur] = True
        word_i.append(cur)

        if Trie.is_word(trie) and len(word_i) >= self.min_len:
            if self.allow_repetitions:
                words.append(word_i)
            else:
                word = self.get_words_str([word_i])[0][0]
                if not self.found.get(word):
                    self.found[word] = True
                    words.append(word_i)

        next_options = self.board.next_options(cur)
        for i in next_options:
            if i in visited:
                continue
            self.dfs(trie, i, visited, words, copy(word_i))
        return words

    def play(self):
        self.found = {}
        start_time = datetime.now()
        result = []
        for i in range(self.board.len):
            words = self.dfs(self.trie.trie, i, {}, [], [])
            if not words:
                continue
            result += words
        logger.info(f"play_finish: found={len(result)}, size={self.board.size}, time={datetime.now() - start_time}")
        return result

    def print_result(self, result):
        to_print = []
        for word in result:
            to_print += self.get_words_str([word])
        print(to_print)

    def get_words_str(self, words_i):
        words = []
        for word_i in words_i:
            word_str = []
            for i in word_i:
                word_str.append(self.board.get_c(i))
            words.append(("".join(word_str), word_i))
        return words


def start():
    board = Board()
    #board.generate_random(1000)
    #board.load_from_file()
    board.load_from_file("random_board.txt")
    trie = Trie()
    #trie.generate_from_dict_file()
    trie.load_from_file()

    game = Game(board, trie, 6)
    result = game.play()
    game.print_result(result)


start()
