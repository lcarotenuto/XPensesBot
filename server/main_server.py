from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
from config import *

class BotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        post_body = str(self.rfile.read(content_length))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Ricevuto " + post_body, "utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer((SERVER['HOSTNAME'], SERVER['PORT']), BotHandler)

    # httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='../res/key.pem', certfile='../res/cert.pem')

    httpd.serve_forever()
