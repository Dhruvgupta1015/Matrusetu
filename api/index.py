import os
import sys

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
    and path mappings resolve reliably regardless of /api prefix stripping
    or literal script destinations.
    """
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            headers = dict(scope.get("headers", []))
            x_matched_path = headers.get(b"x-matched-path", b"").decode("utf-8")

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
