import socket
import threading
from utils import *


bind_ip = socket.gethostname()
bind_port = 7777

def handle_client(client_socket):
    client_socket = Socket_separate(sock=client_socket)
    try:
        msg = client_socket.recv(1024)
        print(msg)
        client_socket.send('ACK, SYN')
        msg = client_socket.recv(1024)
        print(msg)

    finally:
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    try:
        while 1:
            client, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
        print('\r',end='')
    finally:
        server.close()


if __name__ == '__main__':
    main()
