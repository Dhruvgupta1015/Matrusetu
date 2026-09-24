import os
import sys
import urllib.parse

# Add project root and backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
backend_dir = os.path.join(root_dir, "backend")

for p in [root_dir, backend_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from backend.app.main import app as fastapi_app


class VercelAsgiHandler:
    """
    ASGI middleware ensuring that Vercel Serverless Function rewrites
    and path mappings resolve reliably regardless of /api prefix stripping,
    explicit query parameter forwarding, or literal script destinations.
    """
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            query_string = scope.get("query_string", b"").decode("utf-8", errors="replace")
            path = scope.get("path", "")

            # 1. Check for explicit path forwarded via rewrite query param ?__path__=$1
            if "__path__=" in query_string:
                parsed = urllib.parse.parse_qs(query_string, keep_blank_values=True)
                forwarded_path = parsed.pop("__path__", None)
                if forwarded_path and forwarded_path[0]:
                    subpath = forwarded_path[0].lstrip("/")
                    scope["path"] = f"/api/{subpath}"
                    # Reconstruct remaining query string without __path__
                    scope["query_string"] = urllib.parse.urlencode(
                        [(k, v) for k, vs in parsed.items() for v in vs]
                    ).encode("utf-8")
                    return await self.asgi_app(scope, receive, send)

            # 2. Check for Vercel routing headers
            headers = dict(scope.get("headers", []))
            x_matched_path = headers.get(b"x-matched-path", b"").decode("utf-8", errors="replace")

            if path in ("/api/index.py", "/api/index.py/"):
                if x_matched_path and x_matched_path not in ("/api/index.py", "/api/index.py/"):
                    scope["path"] = x_matched_path
                else:
                    scope["path"] = "/api/health"
            elif path.startswith("/api/index.py/"):
                sub = path[len("/api/index.py"):]
                scope["path"] = sub if sub.startswith("/api") else ("/api" + sub)

        return await self.asgi_app(scope, receive, send)


app = VercelAsgiHandler(fastapi_app)
