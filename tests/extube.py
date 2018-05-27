from __future__ import print_function

import fibra

def echo():
    input = fibra.Tube("log_service")
    yield 2
    while True:
        try:
            msg = yield input.pop(wait=True)
        except fibra.EmptyTube:
            print('no message')
            yield 1
        else:
            print(msg)


def send():
    output = fibra.Tube("log_service")
    yield output.push("hello!", wait=False)
    print('pushed')
        

def main():
    """
    >>> main()
    pushed
    pushed
    pushed
    pushed
    pushed
    hello!
    hello!
    hello!
    hello!
    hello!
    """

    schedule = fibra.schedule()
    schedule.install(echo())
    schedule.install(send())
    schedule.install(send())
    schedule.install(send())
    schedule.install(send())
    schedule.install(send())
    schedule.run()

       
if __name__ == '__main__':
    main()
