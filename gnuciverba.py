# this is under GPL v3 license TODO add more details
# author: simone massaro
# mail: massaro.simone.it@gmail.com
"""gnuciverba is a crossword generator
created by mone27 with ale-ci"""

import string # for generating trial version of matrix
import random
import time
import threading
import logging
import numpy as np # not rally necessary but it is nice to use it :D

np.random.seed(5)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class LoadingWidget:
    """this makes rolling widget on cli to show the user that the program is working
    Usage: load_widget = LoadingWidget([message="Loading...])
    start() return immediatly and starts printing on the screen message and the rolling wheel
    stop() stops the wheel to roll

    it can also be used with context manager e.g.
    with LoadingWidget:
        # here do operation while it shows on the screen the rolling wheel
    # here the wheel is stopped
    """

    roll = ['-', '\\', '|', '/']

    def __init__(self, message="Loading..."):
        self.message = message
        self.kill = threading.Event()
        self.thread = threading.Thread(target=self._load, args=(self.kill,))

    def start(self):
        self.thread.start()
        return self

    def stop(self):
        self.kill.set()
        self.thread.join()
        return self

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _load(self, kill_event):
        i = 0
        while not kill_event.wait(0.5):
            if i >= 4:  # 4 is the len of roll not using len(roll) to avoid runtime overhead
                i = 0
            print(f"\r{self.message}{self.roll[i]}", end="")
            i += 1
        print("\r\n") # clears the screen

class Word:
    def __init__(self, word, position, direction):
        self.letters = []
        if direction == 'horizontal':
            x = position[0]
            y = position[1]
            swap = False
        elif direction == 'vertical':
            x = position[1]
            y = position[0]
            swap = True
        else:
            raise ValueError(f"{direction} is not a valid direction")
        self.direction = direction    # not a good idea memory full of useless strings should optimize
        for i,c in enumerate(word):
            pos = [x, y + i]
            if swap: pos[0], pos[1] = pos[1], pos[0]
            self.letters.append((c, pos))

    def __str__(self):
        return ''.join([c[0] for c in self.letters])

    def __repr__(self):
        return str(self)

class Gnuciverba:

    def __init__(self, x: int, y: int, dict_file):
        self.crossword = np.empty((x, y), dtype='<U1')
        self.crossword[:, :] = '#'  # init matrix
        self.x = x
        self.y = y
        self.dict = []
        for length in range(min(x,y), 0, -1):
            with open(dict_file) as f: # TODO optimize not a good idea open file and read it many times
                self.dict.append(np.array([i for i in f.read().splitlines() if len(i) == length]))

        log.debug(f"using this dictionary: {self.dict}")
        self.directions = ['vertical','horizontal']
        self.written_words = []

    def generate(self):
        # put a random word in the crossword
         # maybe not the best place

        for lenght_class in self.dict:
            np.random.shuffle(lenght_class)


        log.debug(f"using this shuffled dictionary: {self.dict}")

        for lenght_class in self.dict:
            for word in lenght_class:
                self._write_word(word)
        return self

    def _write_word(self, word ):

        np.random.shuffle(self.directions)
        for direction in self.directions:   # TODO add randomness
            for column in range(self.y):
                for row in range((self.x - len(word) + 1)):  # every position in the row
                    if self._write_on_crossword(word, (row, column), direction):
                        log.debug(f"written word '{word}' at position ({row},{column}) with direction: {direction}")
                        log.debug(f"crossword now: {self.crossword}")
                        self.written_words.append(Word(word,(row,column), direction))
                        return True
            # log.debug(f"could not write word: {word}")
            return False

    def _write_on_crossword(self, word, start=(0,0), direction='vertical'): # cambai so cavolo di nome che non si capisce niente
        if direction == 'vertical':
            row, column = start
            x, y = self.x, self.y
            x_index = [i for i in range(row, row+len(word))]
            y_index = column
        elif direction == 'horizontal':  # if the other direction swap x and y so to write on rows
            column, row = start
            y, x = self.x, self.y
            y_index = [i for i in range(row, row+len(word))]
            x_index = column
        else:
            raise ValueError("Unsupported direction")

        # TODO write unit tests for this mess
        # check that the word can be replaced
        if len(word) + row  > x:
            # log.debug(f"cannot write: {word} at position ({row},{column}) too long warning this message is wrong!")
            return False # maybe also the type of the error
        old_word = self.crossword[x_index, y_index]

        if self._can_put_string(old_word, word):  # if there is no collision replace the word
            self.crossword[x_index, y_index] = list(word)
            return True
        else:
            return False # if there is a collision so it cannot replace the word

    def _can_put_string(self, old_word, new_word):
        # TODO calculate the number of intersection
        for c1,c2 in zip(old_word, new_word):
           if c2 != c1 and c1 != '#':
                return False
        return True

    def score(self):
        """find the score of the crossword taking into account the number of common letter between words,
         the length of the words and the number of blank places """
        pass

    def _number_common_letters(self) -> int:
        number_letters = 0
        # not a good way for long arrays bad idea to compare with all the words in the crossword
        for first_word in self.written_words:
            for second_word in self.written_words:
                if first_word.letters == second_word.letters : continue  # the two word are the same
                for l in first_word.letters:
                    if l in second_word.letters:
                        number_letters += 1
                        log.debug(f"found common letter between {first_word} and {second_word} at {l} "
                                  f"cross direction: {True if second_word.direction != first_word.direction else False}")
        return number_letters



    def _write_on_row(self, word, start=(0,0)):
        self.crossword[start[0], start[1]:len(word)] = list(word)

    def __str__(self):
        return "".join(" ".join(i)+"\n" for i in self.crossword) + self._get_written_words()

    def __repr__(self):
        return self.__str__()

    def _get_written_words(self):
        words = []
        for word in self.written_words:
            words += ['\t \'', ''.join([i[0] for i in word.letters]), '\' at position: ',str(word.letters[0][1][0]),
                         ' ', str(word.letters[0][1][1]), ' direction: ', word.direction, '\n']
        return ''.join(words)


def get_best_crossword():
    score_max = 0
    loading = LoadingWidget().start()
    for _ in range(200):
        seed = int(time.time())
        np.random.seed(seed)
        cross = Gnuciverba(10, 10, "1000_parole_italiane_comuni.txt").generate()
        score = cross._number_common_letters()
        if score > score_max:
            cross_max = cross
            score_max = score
            i_max = seed

    loading.stop()

    print(cross_max)
    print(score_max)
    print("with random seed:",i_max)


def main_testing():
    logging.basicConfig(level=logging.DEBUG)  # !DEBUG

    with LoadingWidget():
        gnu = Gnuciverba(10, 10, "1000_parole_italiane_comuni.txt")
        gnu.generate()
    print(gnu)
    print(gnu._number_common_letters())

    print("congratulation now you have to find the sense of this crossword")


if __name__ == "__main__":
    main_testing()
    # get_best_crossword()


