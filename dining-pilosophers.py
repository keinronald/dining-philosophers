#!/usr/bin/env python3
"""
Dining philosophers, 5 Philosophers with 5 forks. Must have two forks to eat.

Deadlock is avoided by always trying to grad the fork with the lower id first.
If this fork isn't available the second wont be checked. If the first fork is
available it will be locked and the second fork will be checked. If the second
fork is available it will be locked as well and the philosopher can eat.
Afterwards he releases both forks and is done eating. If the second fork
isn't available we will just check the next philosophers.
"""

import time
import threading


class Philosopher(threading.Thread):
    """
    Attributes:
        name (int): This is the name by witch the philosopher is detected.
        first_fork (thread): left fork.
        second_fork (thread): right fork.
    """
    def __init__(self, name, first_fork, second_fork):
        threading.Thread.__init__(self)
        self.name = name
        self.first_fork = first_fork
        self.second_fork = second_fork
        self.stop = False

    def run(self):
        while not self.stop:
            time.sleep(0.1)  # thinking

            # always start with the fork with the lower id
            if not self.first_fork[1] < self.second_fork[1]:
                self.first_fork, self.second_fork = self.second_fork, self.first_fork

            self.acquire_forks()

    def acquire_forks(self):
        """
        locking the left and the right fork
        :return:
        """
        while not self.stop:
            # lock first fork
            locked_first = self.first_fork[0].acquire()

            if locked_first:
                print(" A -", self.name,
                      "aquired fork #", self.first_fork[1])

                time.sleep(0.1)  # thinking
                locked = self.second_fork[0].acquire()
                if locked:
                    print(" A -", self.name,
                          "aquired fork #", self.second_fork[1])
                    self.eat()

    def eat(self):
        """
        philosopher can finally eat
        and release the forks afterwards
        :return:
        """
        time.sleep(0.1)  # thinking
        print("Philosopher", self.name, "eats")

        self.first_fork[0].release()
        print(" R - Philosopher", self.name,
              "released fork #", self.first_fork[1])

        self.second_fork[0].release()
        print(" R - Philosopher", self.name,
              "released fork #", self.first_fork[1])
        #self.stop = True


def main():
    """
    main function
    :return:
    """
    amount = 5

    # list of forks
    forks = [[threading.Lock(), i] for i in range(amount)]

    philosophers_names = ['Baruch Spinoza', 'Voltaire', 'Laozi', 'Al-Ghazali', 'Sun Tzu']

    # list of philosophers
    philosophers = [Philosopher(philosophers_names[i], forks[i % amount], forks[(i + 1) % amount])
                    for i in range(amount)]

    for philosopher in philosophers:
        philosopher.start()

    time.sleep(3)
    for philosopher in philosophers:
        philosopher.stop = True

    time.sleep(1)
    print("Now we are finishing")


if __name__ == "__main__":
    main()
