# this is under GPL v3 license TODO add more details
# author: simone massaro
# mail: massaro.simone.it@gmail.com
"""gnuciverba is a crossword generator
created by mone27 with ale-ci"""

import string # for generating trial version of matrix
import random
import time
import threading

def caricamento():
    roll = ['-', '\\', '|', '/']

    def _carica():
        while True:
            for i in roll:
                print(f"\rLoading... {i}", end="")
                time.sleep(0.5)
    threading.Thread(target=_carica).start()

class Gnuciverba():

    def __init__(self):
        # generate radom 10x10 matrix
        self.crossword = [[random.choice(string.ascii_lowercase) for _ in range(10)] for _ in range(10)]

    def __str__(self):
        return "".join(" ".join(i)+"\n" for i in self.crossword)
    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    gnu = Gnuciverba()
    print
    caricamento()
    # print(gnu)