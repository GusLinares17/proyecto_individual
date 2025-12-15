from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
import urllib.parse
import pymysql

HOST = "localhost"
PORT = 8000

BASE_DIR = os.getcwd()
STATIC_DIR = os.path.join(BASE_DIR, "static")

def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root1234",
        database="proyecto_cine",
        port=3306
    )

class MiServidor(BaseHTTPRequestHandler):

    def do_GET(self):
        ruta = self.path.split("?")[0]

        if ruta == "/":
            self.servir_archivo(os.path.join(STATIC_DIR, "index.html"))
            return

        if ruta == "/admin":
            self.mostrar_admin()
            return

        if ruta == "/peliculas.json":
            self.servir_archivo(os.path.join(BASE_DIR, "peliculas.json"))
            return

        if ruta.startswith("/static/"):
            archivo = ruta.replace("/static/", "")
            self.servir_archivo(os.path.join(STATIC_DIR, archivo))
            return

        self.enviar_404()

    def do_POST(self):
        if self.path == "/contacto":
            self.procesar_contacto()
            return

        self.enviar_404()

    def servir_archivo(self, ruta):
        if os.path.exists(ruta) and os.path.isfile(ruta):
            tipo_mime = mimetypes.guess_type(ruta)[0]
            if tipo_mime is None:
                tipo_mime = "text/plain"

            self.send_response(200)
            self.send_header("Content-Type", tipo_mime)
            self.end_headers()

            with open(ruta, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.enviar_404()

    def enviar_404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>404 - Archivo no encontrado</h1>")

    def mostrar_admin(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        clave = params.get("pass", [""])[0]

        if clave != "1234":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Acceso denegado</h1>")
            return

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nombre, email, mensaje, fecha FROM mensajes ORDER BY id DESC"
        )
        mensajes = cursor.fetchall()
        cursor.close()
        conexion.close()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Admin</title>
        </head>
        <body style="background:black;color:white;font-family:Arial;padding:20px;">
        <h1>Mensajes recibidos</h1>
        """

        for nombre, email, mensaje, fecha in mensajes:
            html += f"""
            <div style="border:1px solid #444;padding:10px;margin:10px;">
                <p><b>Nombre:</b> {nombre}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Mensaje:</b> {mensaje}</p>
                <p><b>Fecha:</b> {fecha}</p>
            </div>
            """

        html += "</body></html>"

        self.wfile.write(html.encode("utf-8"))

    def procesar_contacto(self):
        longitud = int(self.headers["Content-Length"])
        cuerpo = self.rfile.read(longitud).decode("utf-8")
        datos = urllib.parse.parse_qs(cuerpo)

        nombre = datos.get("nombre", [""])[0]
        email = datos.get("email", [""])[0]
        mensaje = datos.get("mensaje", [""])[0]

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO mensajes (nombre, email, mensaje) VALUES (%s, %s, %s)",
            (nombre, email, mensaje)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>Mensaje recibido correctamente</h1>")

if __name__ == "__main__":
    servidor = HTTPServer((HOST, PORT), MiServidor)
    print(f"Servidor iniciado en http://{HOST}:{PORT}")
    servidor.serve_forever()
