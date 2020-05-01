#!/usr/bin/env python

import argparse
import multiprocessing
import random
import socket
import string
import time


class Process(multiprocessing.Process):
    def __init__(self, id):
        super(Process, self).__init__()
        self.id = id

    def run(self):
        time.sleep(random.randint(0, 1))
        client(self.id)


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Test clients')
    )
    parser.add_argument(
        '--clients',
        dest='clients',
        default=10,
        type=int,
        help='Define number of parallel clients to hit the server',
    )
    parser.add_argument(
        '--loop',
        dest='loop',
        default=1,
        type=int,
        help='Number of times to run the script',
    )
    args = parser.parse_args()
    return args


def random_string():
    string_length = random.randint(1000, 5000)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def client(id):
    client_message = str.encode(random_string())
    server_address = ('test_server', 20001)
    buffer_size = 4096

    UDP_client_socket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_client_socket.sendto(client_message, server_address)

    message_from_server = UDP_client_socket.recvfrom(buffer_size)
    message = ("Client: %s, Server message: %s" %
        (id, message_from_server[0][0:10]))
    print(message)


if __name__ == '__main__':
    args = parse_args()
    for i in range(0, args.loop):
        for j in range(1, args.clients+1):
            p = Process(j)
            p.start()
