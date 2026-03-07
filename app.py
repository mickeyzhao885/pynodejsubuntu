import os
import time
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("SERVER_PORT") or os.environ.get("PORT") or 3000)
WEB_ROOT = os.getcwd()


class RequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        """HEAD health check"""
        if self.path in ["/", "/healthz"]:
            self.send_response(200)
            self.end_headers()
        else:
            file_path = self.translate_path()
            if os.path.exists(file_path):
                self.send_response(200)
            else:
                self.send_response(404)
            self.end_headers()

    def do_GET(self):

        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")
            return

        file_path = self.translate_path()

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "index.html")

        if not os.path.exists(file_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
            print("File read error:", e)

    def translate_path(self):
        path = self.path.split("?", 1)[0]
        path = path.lstrip("/")
        return os.path.join(WEB_ROOT, path)

    def log_message(self, format, *args):
        return


def run_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), RequestHandler)

    print(f"Server running on port {PORT}")
    print("Serving directory:", WEB_ROOT)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
