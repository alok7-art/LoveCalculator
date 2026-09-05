"""
run_web.py
Quick launcher for the web app version of the Love + Aura Calculator.
Starts a local web server and opens index.html in your default web browser!
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

def start_server():
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("💖 LOVE + AURA CALCULATOR - WEB PREVIEW 💖")
        print("=" * 60)
        print(f"Server running at: {url}")
        print("Opening in your browser...")
        print("Press Ctrl+C to stop the server.")
        print("=" * 60)
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped. Bye!")

if __name__ == "__main__":
    start_server()
