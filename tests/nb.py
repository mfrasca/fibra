from __future__ import print_function

import fibra
import time


def blocking_task():
    yield None
    print("I am blocking for 10 seconds.")
    yield fibra.nonblock.Unblock()
    time.sleep(10)
    print("I am about to rejoing the cooperative schedule.")
    yield None

def non_blocking_task():
    for i in range(10):
        print("Non blocking task is running...")
        yield 1.0
    

def main():
    schedule = fibra.schedule()
    schedule.install(non_blocking_task())
    schedule.install(blocking_task())
    schedule.run()

if __name__ == '__main__':
    main()
    
