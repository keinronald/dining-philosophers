#!/usr/bin/env python3
import time
import threading


"""
Dining philosophers, 5 Philosophers with 5 forks. Must have two forks to eat.

Deadlock is avoided by always trying to grad the fork with the lower id first.
If this fork isn't available the second wont be checked. If the first fork is
available it will be locked and the second fork will be checked. If the second
fork is available it will be locked as well and the philosopher can eat.
Afterwards he releases both forks and is done eating. If the second fork
isn't available we will just check the next philosophers.
"""


class Philosopher(threading.Thread):
    def __init__(self, philosopher_id, first_fork, second_fork):
        threading.Thread.__init__(self)
        self.id = philosopher_id
        self.first_fork = first_fork
        self.second_fork = second_fork
        self.stop = False

    def run(self):
        while not self.stop:
            time.sleep(0.1)  # thinking

            if not self.first_fork[1] < self.second_fork[1]:
                self.first_fork, self.second_fork = self.second_fork, self.first_fork

            # lock first fork
            locked_first = self.first_fork[0].acquire()

            if locked_first:
                print(" A - Philosopher", self.id, "aquired fork #", self.first_fork[1])
                self.eat()

    def eat(self):
        while not self.stop:
            time.sleep(0.1)  # thinking
            locked = self.second_fork[0].acquire()
            if locked:
                print(" A - Philosopher", self.id, "aquired fork #", self.second_fork[1])
                time.sleep(0.1)  # thinking

                print("Philosopher", self.id, "EATS")

                self.first_fork[0].release()
                print(" R - Philosopher", self.id, "released fork #", self.first_fork[1])

                self.second_fork[0].release()
                print(" R - Philosopher", self.id, "released fork #", self.first_fork[1])
                self.stop = True


if __name__ == "__main__":
    amount = 5

    # list of forks
    forks = [[threading.Lock(), i] for i in range(amount)]

    # list of philosophers
    philosophers = [Philosopher(i, forks[i % amount], forks[(i + 1) % amount]) for i in range(amount)]

    for p in philosophers:
        p.start()
