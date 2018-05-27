from __future__ import print_function

import fibra

def task_a():
    for i in range(10):
        print('In Task A')
        yield None

def task_b():
    for i in range(10):
        print('In Task B')
        yield None

def main():
    """
    >>> main()
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    In Task A
    In Task B
    """

    s = fibra.schedule()
    s.install(task_a())
    s.install(task_b())
    s.run()


if __name__ == "__main__":
    main()
