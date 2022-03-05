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
            output += '<input name="money" type="text" placeholder="Add some money">'
            output += '<input type="submit" value="Pay">'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

    def do_POST(self):
        if self.path.endswith('/maketransaction'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                amount = fields.get('money')

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 12345))

            if s.recv(1024).decode() == "connected":
                s.send(amount[0].encode())
                newAmount = s.recv(1024).decode()

            s.close()

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.send_header('Location', '/amount')
            output = ''
            output += '<html><body>'
            output += '<h1>The amount of money you entered is</h1>'
            output += '<h1>%s' % newAmount +'</h1'
            output += '</body></html>'

            self.wfile.write(output.encode())

def main():
    PORT = 8000
    server = HTTPServer(('', PORT), helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()