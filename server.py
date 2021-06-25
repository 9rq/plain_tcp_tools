import argparse
import socket
from utils import *


usage = 'server.py -t bind_ip -p port'

def main():
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('--port', '-p', type=int, default=7777)
    parser.add_argument('--target', '-t')
    args = parser.parse_args()

    server = Server(args.target, args.port)
    server.run()


if __name__ == '__main__':
    main()
