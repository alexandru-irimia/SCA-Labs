from socket import *

from Tema1.protocol.utilities import *

pub_key = RSA.importKey(open('server/key.pub', 'rb').read())
private_key = RSA.importKey(open('server/key', 'rb').read())
pg_pub_key = RSA.importKey(open('pg/key.pub', 'rb').read())
client_pub_key = None


def setup_sup_protocol(s: socket):
    print('Setup sub-protocol')
    global client_pub_key
    resp = decrypt(s.recv(2048), private_key)
    client_pub_key = RSA.importKey(resp)
    print(f'From client: {resp}')

    payload = {
        'SID': base64.b64encode(os.urandom(32)).decode()
    }

    s.send(encrypt(json.dumps(payload).encode(), client_pub_key, private_key))


def exchange_sub_protocol(cs: socket, pgs: socket):
    print('Exchange sub-protocol')
    resp = json.loads(decrypt(cs.recv(2048), private_key, client_pub_key))
    print(f'From client: {resp}')

    payload = resp['PM']
    payload = json.dumps(payload).encode()
    pgs.send(encrypt(payload, pg_pub_key, private_key))

    resp = json.loads(decrypt(pgs.recv(2048), private_key, pg_pub_key))
    print(f'From PG: {resp}')

    payload = resp
    payload = json.dumps(payload).encode()
    cs.send(encrypt(payload, client_pub_key, private_key))
