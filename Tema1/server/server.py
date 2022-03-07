import socket

s = socket.socket()
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
    clientAmount = c.recv(1024).decode()
    clientCardNumber = c.recv(1024).decode()
    cardExpirationDate = c.recv(1024).decode()
    cardCvv = c.recv(1024).decode()

    clientAmount += " Dollars"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('127.0.0.1', 12346))

    if server.recv(1024).decode() == "connected":
        server.send(clientCardNumber.encode())
        newCardNumber = server.recv(1024).decode()

    c.send(clientAmount.encode())
    c.send(newCardNumber.encode())

    server.close()
    c.close()
