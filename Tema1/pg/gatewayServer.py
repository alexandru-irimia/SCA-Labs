from Tema1.protocol.pg_protocol import *

s = socket()
print("Socket successfully created")

port = 12346

s.bind(('', port))
print("socket binded to %s" % port)

s.listen(5)
print("socket is listening")

while True:
    c, address = s.accept()
    print('Got connection from', address)

    c.send('connected'.encode())
    exchange_sub_protocol(c)
    c.close()

    c, address = s.accept()
    print('Got connection from', address)

    c.send('connected'.encode())
    resolution_sub_protocol(c)
    c.close()
