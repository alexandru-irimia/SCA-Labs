import base64
import json
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import MD5

block_size = 16
iv = b'\x00' * block_size


def gen_key(key_size: int) -> bytes:
    return os.urandom(key_size)


def create_digital_sign(message: bytes, private_key: RSA.RsaKey) -> bytes:
    h = MD5.new(message)

    rsa = PKCS1_PSS.new(private_key)
    signature = rsa.sign(h)

    return signature


def check_digital_signature(message: bytes, signature: bytes, pub_key: RSA.RsaKey) -> bool:
    h = MD5.new(message)
    rsa = PKCS1_PSS.new(pub_key)

    try:
        rsa.verify(h, signature)
    except ValueError:
        return False
    return True


def encrypt(message: bytes, pub_key: RSA.RsaKey, private_key: RSA.RsaKey = None) -> bytes:
    sym_key = gen_key(block_size)
    cipher_aes = AES.new(sym_key, AES.MODE_CBC, iv)
    ciphertext_aes = cipher_aes.encrypt(pad(message, block_size))

    if private_key is None:
        signature = b''
    else:
        signature = create_digital_sign(message, private_key)

    cipher_rsa = PKCS1_OAEP.new(pub_key)
    ciphertext_rsa = cipher_rsa.encrypt(sym_key)

    ret = {
        'message': base64.b64encode(ciphertext_aes).decode() + '|' + base64.b64encode(signature).decode(),
        'key': base64.b64encode(ciphertext_rsa).decode()
    }

    return json.dumps(ret).encode()


def decrypt(payload: bytes, private_key: RSA.RsaKey, public_key: RSA.RsaKey = None) -> bytes:
    payload = json.loads(payload)
    ciphertext, signature = payload['message'].encode().split(b'|')
    ciphertext = base64.b64decode(ciphertext)
    signature = base64.b64decode(signature)
    key = base64.b64decode(payload['key'])

    cipher_rsa = PKCS1_OAEP.new(private_key)
    key = cipher_rsa.decrypt(key)

    cipher_aes = AES.new(key, AES.MODE_CBC, iv)
    message = unpad(cipher_aes.decrypt(ciphertext), block_size)

    if public_key is not None:
        if not check_digital_signature(message, signature, public_key):
            return b''

    return message
