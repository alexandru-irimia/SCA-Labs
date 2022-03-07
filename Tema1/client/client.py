from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import socket


class helloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/maketransaction'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Enter an amount of money</h1>'

            output += '<form method="POST"enctype="multipart/form-data" action="/maketransaction">'
            output += '<input name="numberCard" type="text" placeholder="Add your card number">'
            output += '<br><br><input name="expirationDate" type="text" placeholder="Expiration Date">'
            output += '<input name="cvv" type="text" placeholder="CVV" style="margin-left: 10px">'
            output += '<br><br><input name="amount" type="text" placeholder="Add some money">'
            output += '<br><br><input type="submit" value="Pay">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

    def do_POST(self):
        if self.path.endswith('/maketransaction'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                amount = fields.get('amount')
                tmpNumberCard = fields.get('numberCard')
                numberCard = ''.join([str(elem) for elem in tmpNumberCard])
                expirationDate = ''.join([str(elem) for elem in fields.get('expirationDate')])
                cvv = ''.join([str(elem) for elem in fields.get('cvv')])


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 12345))

            if s.recv(1024).decode() == "connected":
                s.send(amount[0].encode())
                s.send(numberCard.encode())
                s.send(expirationDate.encode())
                s.send(cvv.encode())

                newAmount = s.recv(1024).decode()
                newCardNumber = s.recv(1024).decode()
            s.close()

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.send_header('Location', '/amount')
            output = ''
            output += '<html><body>'
            output += '<h1>The amount of money you entered is</h1>'
            output += '<h1>%s' % newAmount + '</h1>'
            output += '<h1>%s' % newCardNumber + '</h1>'
            output += '</body></html>'

            self.wfile.write(output.encode())


def main():
    port = 8000
    server = HTTPServer(('', port), helloHandler)
    print('Server running on port %s' % port)
    server.serve_forever()


if __name__ == '__main__':
    main()
