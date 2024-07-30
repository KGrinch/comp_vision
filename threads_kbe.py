from threading import Thread
from time import sleep, perf_counter
import keyboard_emu as kbe


def func(status: callable = None):

    while True:
        position = status()

        if position is None:
            continue

        if True:
            if position > 0:
                kbe.key_down(kbe.SC_RIGHT)
                print('r')
            if position < 0:
                kbe.key_down(kbe.SC_LEFT)
                print('l')


if __name__ == '__main__':
    th = Thread(target=func, args=(lambda: 0,))
    th.start()
