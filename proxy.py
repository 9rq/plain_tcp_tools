# -*- coding: utf-8  -*-
import argparse
import socket
import threading
from utils import *


def proxy_handler(client_socket, **kwargs):
    if kwargs.get('socket_wrapper'):
        client_socket = kwargs.get('socket_wrapper')(sock = client_socket)
    remote_host = kwargs.get('remote_host')
    remote_port = kwargs.get('remote_port')

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    upstream = threading.Thread(target=local2remote, args=(client_socket,remote_socket))
    downstream = threading.Thread(target=remote2local, args=(client_socket,remote_socket))

    upstream.start()
    downstream.start()

    upstream.join()
    downstream.join()
    print('[*] Closed both connections.')

def local2remote(local_socket, remote_socket):
    try:
        while 1:
            local_buffer = receive_from(local_socket)
            if not local_buffer:
                break
            print('[<==] Receive %d bytes from localhost.' % len(local_buffer))
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print('[<==] Sent to remote')
    finally:
        print('[*] No more data. Closing local connections.')
        local_socket.close()

def remote2local(local_socket, remote_socket):
    try:
        while 1:
            remote_buffer = receive_from(remote_socket)
            if not remote_buffer:
                break
            print('[==>] Receive %d bytes from localhost.' % len(remote_buffer))
            hexdump(remote_buffer)
            remote_buffer = request_handler(remote_buffer)

            local_socket.send(remote_buffer)
            print('[==>] Sent to local')
    finally:
        print('[*] No more data. Closing remote connections.')
        remote_socket.close()


def receive_from(connection):
    buffer = b''

    connection.settimeout(10)

    try:
        recv_len = 1
        while recv_len:
            data = connection.recv(4096)
            buffer += data
            recv_len = len(data)
            if recv_len < 4096:
                break
    except Exception as e:
        print(e)
        exit()

    return buffer


def hexdump(src:bytes,length =16):
    print(f'src:{src}')
    result = []
    digits = 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(['{:02X}'.format(x) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append('{:04X}   {}{}    {}'.format(i, hexa, ((length-len(s))*3)*' ', text))

    print('\n'.join(result))


def request_handler(buffer):
    return buffer


def response_handler(buffer):
    return buffer


def main():
    usage = 'Usage: python proxy.py [localhost] [localport] [remotehost] [remoteport]\n Example: python proxy.py 127.0.0.1 9000 10.12.132.1 9000'
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('localhost')
    parser.add_argument('localport', type=int)
    parser.add_argument('remotehost')
    parser.add_argument('remoteport', type=int)
    args = parser.parse_args()

    server = Server(args.localhost, args.localport)
    server.run(handler=proxy_handler, remote_host=args.remotehost, remote_port=args.remoteport,)

main()
