from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from Tema1.protocol.client_protocol import *


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
            output = ''
            output += '<html><body>'

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                amount = fields.get('amount')
                tmp_number_card = fields.get('numberCard')
                number_card = ''.join([str(elem) for elem in tmp_number_card])
                expiration_date = ''.join([str(elem) for elem in fields.get('expirationDate')])
                cvv = ''.join([str(elem) for elem in fields.get('cvv')])

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('127.0.0.1', 12345))

            if s.recv(1024).decode() == "connected":
                resp = setup_sub_protocol(s)
                output += '<h3>Setup sub-protocol: %s' % resp + '</h3>'
                resp = json.loads(resp)
                payload = {
                    'PM': {
                        'PI': {
                            'CardN': number_card,
                            'CardExp': expiration_date,
                            'CCode': cvv,
                            'SID': resp['SID'],
                            'Amount': amount
                        }
                    },
                    'PO': {
                        'OrderDesc': 'buy',
                        'SID': resp['SID'],
                        'Amount': amount
                    }
                }
                resp = exchange_sub_protocol(json.dumps(payload).encode(), s)
                output += '<h3>Exchange sub-protocol: %s' % resp + '</h3>'
                resp = json.loads(resp)

                pg = socket(AF_INET, SOCK_STREAM)
                pg.connect(('127.0.0.1', 12346))
                payload = {
                    'SID': resp['SID'],
                    'Amount': amount,
                    'key': open('client/key.pub', 'rb').read().decode()
                }
                if pg.recv(1024).decode() == "connected":
                    output += '<h3>Resolution sub-protocol: %s' % resolution_sub_protocol(json.dumps(payload).encode(),
                                                                                          pg) + '</h3>'
            s.close()

            output += '</body></html>'

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            self.send_header('Location', '/amount')

            self.wfile.write(output.encode())


def main():
    port = 8000
    server = HTTPServer(('', port), helloHandler)
    print('Server running on port %s' % port)
    server.serve_forever()


if __name__ == '__main__':
    main()
