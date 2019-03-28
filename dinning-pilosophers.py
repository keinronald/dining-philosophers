#!/usr/bin/env python3
import time


def philosopher(stop, first_fork, second_fork):
    while not stop.is_set():
        time.sleep(0.1)  # thinking
        acquire first_fork

        time.sleep(0.1)  # thinking
        aquire second_fork

        time.sleep(0.1)  # thinking
        print("eat")
        release first_fork
        release second_fork


if __name__ == "__main__":                     # If called from interpreter
    print("HI")

