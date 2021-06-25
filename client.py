import argparse
from utils import *


host = socket.gethostname()
port = 7777

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', '-t', required=True)
    parser.add_argument('--port', '-p', type=int, required=True)
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
