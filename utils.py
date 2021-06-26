import socket
import threading


# legacy socket wrapper implementation class Socket_separate:
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


# recommending socket wrapper
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

    def recv(self)->str:
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

    def __getattr__(self,name):
        return object.__getattribute__(self.sock, name)


class Server():
    def __init__(self, bind_ip, bind_port):
        self.bind_ip = bind_ip or socket.gethostname()
        self.bind_port = bind_port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.bind_ip, self.bind_port))
        except:
            print('[!!] Failed to listen on %s:%d' % (self.bind_ip,self.bind_port))
            print('[!!] Check for other listening sockets or correct permissions')
            exit()


    def run(self, **kwargs):
        handler = kwargs.get('handler') or self.default_handler
        print('[*] Listening on %s:%d' % (self.bind_ip, self.bind_port))

        self.server.listen(5)
        try:
            while 1:
                client, addr = self.server.accept()
                print('[*] Recieved incoming connection from %s:%d' % (addr[0], addr[1]))
                # wrap
                client_handler = threading.Thread(target=handler,args=(client, ),kwargs=kwargs)
                client_handler.start()
        except KeyboardInterrupt:
            print('\r',end='')
        finally:
            self.server.close()

    def default_handler(self, client_socket, **kwargs):
        if kwargs.get('socket_wrapper'):
            client_socket = kwargs.get('socket_wrapper')(sock = client_socket)
        try:
            msg = client_socket.recv()
            print(msg)
            client_socket.send('ACK, SYN')
            msg = client_socket.recv()
            print(msg)

        finally:
            client_socket.close()
