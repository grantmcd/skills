import http.server
import os
import secrets
import socketserver
import sys

PORT = 8080
SIGNAL_FILE = "approval_signal.txt"
TOKEN_FILE = "session_token.txt"


class AuthenticatedApprovalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse token from query string
        try:
            query = self.path.split("?")[1]
            params = dict(p.split("=") for p in query.split("&"))
            provided_token = params.get("token")
        except Exception:
            provided_token = None

        with open(TOKEN_FILE, "r") as f:
            valid_token = f.read().strip()

        if self.path.startswith("/approve") and provided_token == valid_token:
            with open(SIGNAL_FILE, "w") as f:
                f.write(f"APPROVED:{provided_token}")

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Security Verified. Approval received.")

            print("Authenticated approval signal captured. Shutting down...")
            sys.exit(0)
        else:
            self.send_response(403)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Forbidden: Invalid or missing security token.")

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    # Generate a fresh session token
    token = secrets.token_urlsafe(16)
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

    if os.path.exists(SIGNAL_FILE):
        os.remove(SIGNAL_FILE)

    print(f"Secure approval listener active on port {PORT}...")
    with socketserver.TCPServer(("", PORT), AuthenticatedApprovalHandler) as httpd:
        try:
            httpd.serve_forever()
        except SystemExit:
            pass
