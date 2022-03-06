from socket import socket

from utilities import *

pub_key = RSA.importKey(open('../server/key.pub', 'rb').read())
private_key = RSA.importKey(open('../server/key', 'rb').read())
pg_pub_key = RSA.importKey(open('../pg/key.pub', 'rb').read())
client_pub_key = RSA.RsaKey()


def server_setup_sup_protocol(s: socket):
    global client_pub_key
    resp = decrypt(s.recv(2048), private_key)
    client_pub_key = RSA.importKey(resp)

    s.send(encrypt(json.dumps({
        'resp': 'OK',
        'sid': os.urandom(32)
    }).encode(), client_pub_key, private_key))


def exchange_sub_protocol(cs: socket, pgs: socket):
    resp = json.loads(decrypt(cs.recv(2048), private_key, client_pub_key))
    print(resp)

    payload = {}
    payload = json.dumps(payload).encode()
    pgs.send(encrypt(payload, pg_pub_key, private_key))

    resp = json.loads(decrypt(pgs.recv(2048), private_key, pg_pub_key))
    print(resp)

    payload = {}
    payload = json.dumps(payload).encode()
    cs.send(encrypt(payload, client_pub_key, private_key))
