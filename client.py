import argparse
import socket
from utils import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', '-t', default=socket.gethostname())
    parser.add_argument('--port', '-p', type=int, default=7777)
    args = parser.parse_args()

    try:
        sock = Socket_Sign()
        sock.connect((args.target,args.port))
        sock.send('SYN')
        msg = sock.recv()
        print(msg)
        sock.send('ACK')
    finally:
        sock.close()


if __name__ == '__main__':
    main()
