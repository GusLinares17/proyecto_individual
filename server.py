from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import pymysql   # <-- para MySQL

PUERTO = 8000

# =======================================
#  FUNCIÓN DE CONEXIÓN (simple)
# =======================================
def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root1234",  # tu clave
        database="proyecto_cine",
        port=3306
    )


class MiServidor(BaseHTTPRequestHandler):

    # =======================================
    #                  GET
    # =======================================
    def do_GET(self):

        ruta = self.path.split("?")[0]

        if ruta == "/":
            self.send_response(302)
            self.send_header("Location", "/static/index.html")
            self.end_headers()
            return

        # ------------------------------
        #      ADMIN PROTEGIDO
        # ------------------------------
        if ruta == "/admin":
            self.mostrar_admin()
            return

        if ruta == "/peliculas.json":
            with open("peliculas.json", "rb") as f:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f.read())
            return

        if ruta.startswith("/static/"):
            archivo = "." + ruta
            with open(archivo, "rb") as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
            return

    # =======================================
    #       FUNCIÓN PARA /admin
    # =======================================
    def mostrar_admin(self):

        # Obtener contraseña ?pass=1234
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        clave = params.get("pass", [""])[0]

        if clave != "1234":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Acceso denegado</h1>")
            return

        # Leer mensajes desde MySQL
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, email, mensaje, fecha FROM mensajes ORDER BY id DESC")
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()

        # Crear HTML simple
        html = """
        <html>
        <head><meta charset='UTF-8'><title>Admin</title></head>
        <body style='background:black;color:white;font-family:Arial;padding:20px;'>
        <h1>Mensajes recibidos</h1>
        """

        for nombre, email, mensaje, fecha in filas:
            html += f"""
            <div style='border:1px solid #444;padding:10px;margin:10px;'>
                <p><b>Nombre:</b> {nombre}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Mensaje:</b> {mensaje}</p>
                <p><b>Fecha:</b> {fecha}</p>
            </div>
            """

        html += "</body></html>"

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


    # =======================================
    #                 POST
    # =======================================
    def do_POST(self):

        if self.path == "/contacto":

            longitud = int(self.headers["Content-Length"])
            cuerpo = self.rfile.read(longitud).decode("utf-8")
            datos = urllib.parse.parse_qs(cuerpo)

            nombre = datos.get("nombre", [""])[0]
            email  = datos.get("email", [""])[0]
            mensaje = datos.get("mensaje", [""])[0]

            print("===== FORMULARIO =====")
            print("Nombre:", nombre)
            print("Email:", email)
            print("Mensaje:", mensaje)

            # Guardar en MySQL
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO mensajes (nombre, email, mensaje) VALUES (%s, %s, %s)",
                (nombre, email, mensaje)
            )
            conexion.commit()
            cursor.close()
            conexion.close()

            # Respuesta simple
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Mensaje recibido correctamente!</h1>")
            return


# =======================================
#        INICIAR SERVIDOR
# =======================================
with HTTPServer(("", PUERTO), MiServidor) as servidor:
    print("Servidor activo en puerto", PUERTO)
    servidor.serve_forever()
