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


class Gnuciverba:

    def __init__(self, x: int, y: int, dict_file):
        # generate random x*y matrix
        self.crossword = np.array([[random.choice(string.ascii_lowercase) for _ in range(x)] for _ in range(y)])
        with open(dict_file) as f:
            self.dict = {i for i in f.read().splitlines() if len(i) <= min(x, y)}  # removes words that are too long

        log.debug(f"using this dictionary: {self.dict}")
        self._write_on_row("ciao")
        self._write_on_column("bene")

        # it takes a random word and put it in a random position
    def _write_on_column(self, word, start=(0,0)):  # maybe add type notations
        self.crossword[start[0]:len(word), start[1]] = list(word)

    def _write_on_row(self, word, start=(0,0)):
        self.crossword[start[0], start[1]:len(word)] = list(word)

    def __str__(self):
        return "".join(" ".join(i)+"\n" for i in self.crossword)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    with LoadingWidget():
        gnu = Gnuciverba(5, 5, "1000_parole_italiane_comuni.txt")
    print(gnu)

    print("congratulation now you have to find the sense of this crossword")

