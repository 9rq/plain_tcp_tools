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
    def __init__(self, sock=None, digit=4):
        '''
        digit: digit of len(msg)

        digit = 4 means len(msg) < 4 bytes (uint)
        '''

        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buff = b''
        self.digit = digit

    def connect(self, target):
        self.sock.connect(target)

    def close(self):
        self.sock.close()

    def send(self, msg:str):
        msg = msg.encode()
        msg_len = len(msg)
        self.__send(self.int2bytes(msg_len))
        self.__send(msg)

    def __send(self, msg:bytes):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError('[!] socket connection broken')
            totalsent += sent

    def recv(self, buff_size:int)->str:
        msg_len = self.bytes2int(self.__recv(self.digit))
        msg = self.__recv(msg_len).decode()
        return msg

    def __recv(self, buff_size:int)->bytes:
        while 1:
            if len(self.buff) >= buff_size:
                break
            data = self.sock.recv(buff_size)
            if data == b'':
                raise RuntimeError('[!] socket connection broken')
            self.buff += data
        msg = self.buff[:buff_size]
        self.buff = self.buff[buff_size:]
        return msg

    def int2bytes(self, num:int):
        return num.to_bytes(self.digit, 'big')

    def bytes2int(self, num:bytes):
        return int.from_bytes(num, 'big')
