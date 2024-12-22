from http.server import SimpleHTTPRequestHandler, HTTPServer
from gpiozero import LED

red = LED(17)

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/led/on':
            print("Turning LED ON")
            red.on()
        if self.path == '/led/off':
            print("Turning LED OFF")
            red.off()
        self.send_response(200)
        self.end_headers()

httpd = HTTPServer(("", 8080), MyHandler)
httpd.serve_forever()
