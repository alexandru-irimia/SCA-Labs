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
    clientMessage = c.recv(1024).decode()
    clientMessage += " Dollars"
    c.send(clientMessage.encode())
    c.close()
