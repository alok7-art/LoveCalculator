"""
server.py
Production-ready HTTP server for Render deployment.
Serves index.html, audio assets, and an optional /api/calculate endpoint.
Uses 100% Python standard library (no pip install required).
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from love_calculator import calculate_profile

PORT = int(os.environ.get("PORT", 8080))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class LoveCalculatorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # API endpoint: /api/calculate?name1=...&gender1=...&name2=...&gender2=...
        if parsed.path == "/api/calculate":
            query_params = urllib.parse.parse_qs(parsed.query)
            name1 = query_params.get("name1", [""])[0]
            gender1 = query_params.get("gender1", ["other"])[0]
            name2 = query_params.get("name2", [""])[0]
            gender2 = query_params.get("gender2", ["other"])[0]

            if not name1 or not name2:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "name1 and name2 are required"}).encode("utf-8"))
                return

            result = calculate_profile(name1, gender1, name2, gender2)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        # Default: Serve static files (index.html, song_*.wav, etc.)
        return super().do_GET()


def run():
    # Allow socket address reuse so restarts are instantaneous
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), LoveCalculatorHandler) as httpd:
        print(f"Serving Love + Aura Calculator on port {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    run()
