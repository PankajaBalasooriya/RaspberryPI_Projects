from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/led/on':
            # LED code
            pass
        self.send_response(200)
        self.end_headers()


httpd = HTTPServer(("", 8080), MyHandler)
httpd.serve_forever()            