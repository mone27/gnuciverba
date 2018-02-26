# this is under GPL v3 license TODO add more details
# author: simone massaro
# mail: massaro.simone.it@gmail.com
"""gnuciverba is a crossword generator
created by mone27 with ale-ci"""

import string # for generating trial version of matrix
import random
import time
import threading


class LoadingWidget:


    # class _Load(threading.Thread):
    #     """Thread class with a stop() method. The thread itself has to check
    #     regularly for the stopped() condition."""
    #
    #     def __init__(self):
    #         super(_Load, self).__init__()
    #         self._stop_event = threading.Event()
    #
    #     def stop(self):
    #         self._stop_event.set()
    #
    #     def stopped(self):
    #         return self._stop_event.is_set()

    roll = ['-', '\\', '|', '/']

    def __init__(self):
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
            print(f"\rLoading... {self.roll[i]}", end="")
            i += 1
        print("\r\n") # clears the screen



class Gnuciverba:

    def __init__(self, x: int, y: int):
        # generate random x*y matrix
        self.crossword = [[random.choice(string.ascii_lowercase) for _ in range(x)] for _ in range(y)]

    def __str__(self):
        return "".join(" ".join(i)+"\n" for i in self.crossword)
    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    load = LoadingWidget().start()
    gnu = Gnuciverba(20, 20)
    time.sleep(10)
    load.stop()
    print(gnu)
    with LoadingWidget():
        time.sleep(5)
    print("congratulation now you have to find the sense of this crossword")

