from socket import socket

from utilities import *

pub_key = RSA.importKey(open('../server/key.pub', 'rb').read())
private_key = RSA.importKey(open('../server/key', 'rb').read())
client_pub_key = RSA.importKey(open('../client/key.pub', 'rb').read())
server_pub_key = RSA.importKey(open('../server/key.pub', 'rb').read())


def exchange_sub_protocol(s: socket):
    resp = decrypt(s.recv(2048), private_key, server_pub_key)
    resp = json.loads(resp)
    print(resp)

    payload = {}
    payload = json.dumps(payload).encode()
    s.send(encrypt(payload, server_pub_key, private_key))


def resolution_sub_protocol(s: socket):
    resp = decrypt(s.recv(2048), private_key, client_pub_key)
    resp = json.loads(resp)
    print(resp)

    payload = {}
    payload = json.dumps(payload).encode()
    s.send(encrypt(payload, client_pub_key, private_key))
