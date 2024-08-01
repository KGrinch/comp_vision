from threading import Thread
from time import sleep, perf_counter
import keyboard_emu as kbe


def ret_track(direction):
    if direction == 'r':
        kbe.key_press(kbe.SC_RIGHT, interval=1)
    if direction == 'l':
        kbe.key_press(kbe.SC_LEFT, interval=1)


def steer(status: callable = None):

    while True:
        position = status()

        if position is None:
            continue
        # cnt = 0
        # old_pos = None
        if True:
            # if position == old_pos:
            #    cnt += 1
            if position >= 50:
                kbe.key_down(kbe.SC_RIGHT)
                sleep(0.5)
                kbe.key_up(kbe.SC_RIGHT)
            elif 50 > position > 0:
                kbe.key_press(kbe.SC_RIGHT, interval=0.01)
                # position = 0
                # print('r')
            #    if cnt == 10:
            #        ret_track('r')
            elif position <= -50:
                kbe.key_down(kbe.SC_LEFT)
                sleep(0.5)
                kbe.key_up(kbe.SC_LEFT)
            if -50 < position < 0:
                kbe.key_press(kbe.SC_LEFT, interval=0.01)
                # position = 0
                # print('l')
            #    if cnt == 10:
            #        ret_track('l')
            # old_pos = position


if __name__ == '__main__':
    th = Thread(target=steer, args=(lambda: 0,))
    th.start()