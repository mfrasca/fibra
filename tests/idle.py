from __future__ import print_function

import fibra


def task_a():
    for i in range(5):
        print('Task A is going to sleep.')
        yield 1.0
        print('Task A is awake.')
        yield None

def task_b():
    print("Task B is sleeping for 10 seconds.")
    yield 10.0
    print('Task B is awake.')

def task_c():
    for i in range(100):
        yield None

def task_d():
    for i in range(10):
        yield None

idle_count = 0
def idle():
    global idle_count
    idle_count += 1
    

def main():
    """
    >>> main()  # doctest: +ELLIPSIS
    Task A is going to sleep.
    Task B is sleeping for 10 seconds.
    Task A is awake.
    Task A is going to sleep.
    Task A is awake.
    Task A is going to sleep.
    Task A is awake.
    Task A is going to sleep.
    Task A is awake.
    Task A is going to sleep.
    Task A is awake.
    Task B is awake.
    Idle was called ... times. (Should be >> 1)
    Idle was called 100 times. (Should be 100)

    """
    global idle_count
    s = fibra.schedule()
    s.install(task_a())
    s.install(task_b())
    s.register_idle_func(idle)
    s.run()
    print("Idle was called", idle_count, "times. (Should be >> 1)")
    idle_count = 0
    s.install(task_c())
    s.install(task_d())
    s.run()
    print("Idle was called", idle_count, "times. (Should be 100)")


if __name__ == "__main__":
    main()
