from utils import *


host = socket.gethostname()
port = 7777

def main():
    try:
        sock = Socket_Sign()
        sock.connect((host,port))
        sock.send('SYN'*10)
        msg = sock.recv()
        print(msg)
        sock.send('ACK')
    finally:
        sock.close()


if __name__ == '__main__':
    main()
