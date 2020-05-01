#!/usr/bin/env python

import argparse
import graphyte
import random
import socket
import string
import sys
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Test server')
    )
    parser.add_argument(
        '--bitrate',
        dest='bitrate',
        default=1,
        type=int,
        help='Target bitrate to be sent to client',
    )
    args = parser.parse_args()
    return args


def random_string():
    string_length = random.randint(1000, 5000)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def server(args):
    server_IP = '0.0.0.0'
    server_port = 20001
    buffer_size = 4096

    UDP_server_socket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_server_socket.bind((server_IP, server_port))

    while(True):
        received = UDP_server_socket.recvfrom(buffer_size)
        raw_message, raw_address = received[0], received[1]
        client_message = "Client message length: %d" % (len(raw_message))
        client_IP = ("Client IP Address: %s:%s" %
            (raw_address[0], raw_address[1]))

        server_message = str.encode(random_string())
        UDP_server_socket.sendto(server_message, raw_address)
        time.sleep(args.bitrate)

        graphyte.send('trigger_count', 1)
        graphyte.send('client_msg_length', len(raw_message))
        graphyte.send('server_msg_length', len(server_message))
        print("%s, %s, Server message length: %d" %
            (client_message, client_IP, len(server_message)))


if __name__ == '__main__':
    graphyte.init('graphite', port=2003)
    args = parse_args()
    server(args)
