import socket


class Socket_separate:
    def __init__(self, sock=None):
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buff = b''

    def connect(self, target):
        self.sock.connect(target)

    def close(self):
        self.sock.close()

    def send(self, msg:str, sep:str='\r\n'):
        totalsent = 0
        msg += sep
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError('[!] socket connection broken')
            totalsent += sent

    def recv(self, buff_size:int, sep:str='\r\n'):
        while 1:
            buff_split = self.buff.split(sep.encode(), 1)
            if len(buff_split) ==2:
                break
            data = self.sock.recv(buff_size)
            if data == b'':
                raise RuntimeError('[!] socket connection broken')
            self.buff += data
            print('continue')
        msg, self.buff = buff_split
        return msg.decode()


class Socket_Sign:
    # sturct.pack('!i', 100)などを使ってint2bytesする？
    def __init__(self, sock=None):
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buff = b''

    def connect(self, target):
        self.sock.connect(target)

    def close(self):
        self.sock.close()

    def send(self, msg:str):
        msg_len = len(msg)
        self.__send()
        pass

    def __send(self, msg:bytes):
        # msg need to be bytes object
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError('[!] socket connection broken')
            totalsent += sent

    def recv(self, buff_size:int):
        pass
