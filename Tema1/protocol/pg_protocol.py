from socket import *

from Tema1.protocol.utilities import *

pub_key = RSA.importKey(open('../pg/key.pub', 'rb').read())
private_key = RSA.importKey(open('../pg/key', 'rb').read())
client_pub_key = RSA.importKey(open('../client/key.pub', 'rb').read())
server_pub_key = RSA.importKey(open('../server/key.pub', 'rb').read())


def exchange_sub_protocol(s: socket):
    print('Exchange sub-protocol')
    resp = decrypt(s.recv(2048), private_key, server_pub_key)
    resp = json.loads(resp)
    print(f'From merchant: {resp}')

    payload = {
        'Resp': 'OK',
        'SID': resp['PI']['SID']
    }
    payload = json.dumps(payload).encode()
    s.send(encrypt(payload, server_pub_key, private_key))


def resolution_sub_protocol(s: socket):
    print('Resolution sub-protocol')
    global client_pub_key
    resp = decrypt(s.recv(2048), private_key, client_pub_key)
    resp = json.loads(resp)
    print(f'From client: {resp}')

    payload = {
        'Resp': 'OK',
        'SID': resp['SID']
    }
    payload = json.dumps(payload).encode()
    client_pub_key = RSA.importKey(resp['key'])
    s.send(encrypt(payload, client_pub_key, private_key))
