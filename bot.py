import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request

# Servidor HTTP básico con soporte de Proxy para canales en vivo
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/proxy':
            query_params = parse_qs(parsed_path.query)
            target_url = query_params.get('url', [None])[0]
            if not target_url:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing url")
                return
            try:
                req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    self.send_response(response.status)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Headers', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"PelisFull Proxy & Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

if __name__ == '__main__':
    t = threading.Thread(target=run_web_server)
    t.start()
    print("Servidor Proxy y Web iniciado correctamente.")
