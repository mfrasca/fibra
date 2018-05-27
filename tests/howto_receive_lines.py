from __future__ import print_function

import fibra
import fibra.net

def task(sock, address):
    #create a tasks which returns lines from a socket    
    line_receiver = fibra.net.recv_lines(sock)
    while True:
        #receive a line
        line = yield line_receiver
        print("Received:", line)


def main():
    s = fibra.schedule()
    #install a task which installs a new task on a new connection
    s.install(fibra.net.listen(("localhost", 2000), task))
    s.run()

if __name__ == '__main__':
    main()
    
    
