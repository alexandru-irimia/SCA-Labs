from socket import *

from Tema1.protocol.utilities import *

pub_key = RSA.importKey(open('client/key.pub', 'rb').read())
private_key = RSA.importKey(open('client/key', 'rb').read())
server_pub_key = RSA.importKey(open('server/key.pub', 'rb').read())
pg_pub_key = RSA.importKey(open('pg/key.pub', 'rb').read())


def setup_sub_protocol(s: socket) -> str:
    print('Setup sub-protocol')
    ret = ''
    s.send(encrypt(open('client/key.pub', 'rb').read(), server_pub_key))
    resp = decrypt(s.recv(2048), private_key, server_pub_key)
    ret += resp.decode()
    resp = json.loads(resp)
    print(f'From merchant: {resp}')

    return ret


def exchange_sub_protocol(payload: bytes, s: socket) -> str:
    print('Exchange sub-protocol')
    ret = ''
    s.send(encrypt(payload, server_pub_key, private_key))

    resp = decrypt(s.recv(2048), private_key, server_pub_key)
    ret += resp.decode()
    resp = json.loads(resp)
    print(f'From merchant: {resp}')

    return ret


def resolution_sub_protocol(payload: bytes, s: socket) -> str:
    print('Resolution sub-protocol')
    ret = ''
    s.send(encrypt(payload, pg_pub_key, private_key))

    resp = decrypt(s.recv(2048), private_key, pg_pub_key)
    ret += resp.decode()
    resp = json.loads(resp)

    print(f'From PG: {resp}')

    return resp
