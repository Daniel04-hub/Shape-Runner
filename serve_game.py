import http.server
import socketserver
import mimetypes
import os

# Define the port
PORT = 8090

# Define the directory to serve (The build folder)
WEB_DIR = os.path.join(os.getcwd(), 'web_build', 'build', 'web')

# Explicitly set MIME types to avoid Windows Registry issues
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/javascript', '.js')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

print(f"Starting server for directory: {WEB_DIR}")
print(f"Open your browser to: http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
