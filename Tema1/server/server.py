from Tema1.protocol.server_protocol import *

s = socket()
print("Socket successfully created")

port = 12345

s.bind(('', port))
print("socket binded to %s" % (port))

s.listen(5)
print("socket is listening")

while True:
    c, address = s.accept()
    print('Got connection from', address)

    c.send('connected'.encode())

    setup_sup_protocol(c)

    server = socket(AF_INET, SOCK_STREAM)
    server.connect(('127.0.0.1', 12346))

    if server.recv(1024).decode() == "connected":
        exchange_sub_protocol(c, server)

    server.close()
    c.close()
