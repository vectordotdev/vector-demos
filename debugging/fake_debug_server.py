import http.server
import socketserver
import json
import threading
import zlib
from http import HTTPStatus  # Import HTTP status codes

# Global variable for the response code
response_code = HTTPStatus.OK  # Default to 200 OK

class DebuggingHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    HTTP server for debugging.

    - Responds with a dynamically controlled status code (default HTTPStatus.OK).
    - Supports GET, POST, PUT, DELETE, and other HTTP methods.
    - Allows changing the response code via a POST request to /set_status.
    - Logs request headers and JSON payloads (supports zlib-compressed payloads).
    """

    def do_GET(self):
        """Handles GET requests by returning the configured response code."""
        self.send_custom_response()

    def do_POST(self):
        """Handles POST requests. Logs request details before checking the path."""
        json_data = self.log_request_details()
        if self.path == "/set_status":
            self.set_status(json_data)
        elif self.path == "/logs":
            self.send_custom_response()

    def do_PUT(self):
        """Handles PUT requests."""
        self.send_custom_response()

    def do_DELETE(self):
        """Handles DELETE requests."""
        self.send_custom_response()

    def send_custom_response(self):
        """Send an HTTP response with the currently configured status code."""
        global response_code
        self.send_response(response_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"status": response_code, "message": f"Responding with {response_code}"}
        self.wfile.write(json.dumps(response).encode())

    def log_request_details(self):
        """Logs headers and JSON payload for all POST requests before processing."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        print("\n📥 Received POST request:")
        print(f"🔗 Path: {self.path}")
        print("📜 Headers:")
        for key, value in self.headers.items():
            print(f"   {key}: {value}")

        if self.headers.get('Content-Encoding') == 'gzip':
            print("❌ Error: Gzip compression is not supported.")
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Gzip compression is not supported."}).encode())
            return None

        if self.headers.get('Content-Encoding') == 'deflate':
            try:
                body = zlib.decompress(body)
                print("🗜️ Payload was zlib-compressed. Decompressed successfully.")
            except zlib.error:
                print("❌ Error decompressing zlib payload.")
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid zlib-compressed data"}).encode())
                return None

        try:
            json_data = json.loads(body.decode())
            print("📦 JSON Payload:", json.dumps(json_data, indent=2))
            return json_data
        except json.JSONDecodeError:
            print("⚠️  No valid JSON payload received.")
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid zlib-compressed data"}).encode())
            return None

    def set_status(self, json_data):
        """Handles POST /set_status to update the response code dynamically."""
        global response_code

        if json_data is None:
            self.send_response(HTTPStatus.BAD_REQUEST)
            response = {"error": "Invalid request format. Send JSON with {'status': <code>}."}
        else:
            try:
                new_status = int(json_data.get("status", HTTPStatus.OK))
                if HTTPStatus.CONTINUE <= new_status <= HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED:
                    response_code = new_status
                    self.send_response(HTTPStatus.OK)
                    response = {"message": f"Response code updated to {response_code}"}
                else:
                    self.send_response(HTTPStatus.BAD_REQUEST)
                    response = {"error": "Invalid status code. Must be between 100 and 599."}
            except ValueError:
                self.send_response(HTTPStatus.BAD_REQUEST)
                response = {"error": "Invalid status code format."}

        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def run_server(port):
    """Starts the HTTP server on the specified port."""
    handler = DebuggingHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 Serving on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    port = 8000
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Server shutting down.")