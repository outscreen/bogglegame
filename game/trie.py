import json
import os
from logger import logging

logger = logging.getLogger("trie")


class Trie:
    END_OF_WORD = "!"

    def __init__(self):
        self._trie = {}

    @property
    def trie(self):
        return self._trie

    def save_to_file(self, path="trie.json"):
        with open(path, 'w') as outfile:
            json.dump(self._trie, outfile)
        logger.info(f"save: location={path}, size={os.stat(path).st_size}")
        return path

    def load_from_file(self, path="trie.json"):
        with open(path) as json_file:
            self._trie = json.load(json_file)
        logger.info(f"load: location={path}, size={os.stat(path).st_size}")
        return path

    def generate_from_dict_file(self, dict_path="dictionary.txt", trie_path="trie.json"):
        file = open(dict_path, "r")
        count = 0
        while True:
            count += 1
            line = file.readline()
            # end of file
            if not line:
                break
            word = line.strip().lower()
            # empty sting
            if not word:
                continue
            self.add_word(word)
        file.close()
        trie_path = self.save_to_file(trie_path)
        logger.info(f"create_from_dict_file: word_count={count}, trie_path={trie_path}, dict_path={dict_path}")

    def add_words(self, words):
        for word in words:
            self._add_word(word)

    def add_word(self, word):
        trie = self._trie
        for c in word:
            trie.setdefault(c, {})
            trie = trie[c]
        trie[Trie.END_OF_WORD] = True

    @staticmethod
    def is_word(trie):
        return bool(trie.get(Trie.END_OF_WORD))
