import http.server
import socketserver
import os

PUERTO = 8000

ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(ROOT, "static")


class MiHandler(http.server.SimpleHTTPRequestHandler):

    def translate_path(self, path):

        # Página principal
        if path == "/" or path == "/index.html":
            return os.path.join(STATIC_DIR, "pages", "index.html")

        # Archivos dentro de /static/
        if path.startswith("/static/"):
            return os.path.join(ROOT, path[1:])

        # Todas las páginas HTML dentro de /static/pages/
        paginas = [
            "index.html",
            "peliculas.html",
            "curiosidades.html",
            "contacto.html",
            "admin.html",
            "detalle.html"
        ]

        archivo = path.lstrip("/")

        if archivo in paginas:
            return os.path.join(STATIC_DIR, "pages", archivo)

        # Si la ruta no coincide → 404
        return ""

    def send_error(self, code, message=None):
        if code == 404:
            self.error_message_format = "<h1>Ruta no válida</h1>"
        super().send_error(code, message)


with socketserver.TCPServer(("localhost", PUERTO), MiHandler) as httpd:
    print(f"\nServidor iniciado en http://localhost:{PUERTO}\n")
    httpd.serve_forever()
