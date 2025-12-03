// Obtener el ID desde la URL
const params = new URLSearchParams(window.location.search);
const id = params.get("id");

// Cargar JSON
fetch("/peliculas.json")
    .then(res => res.json())
    .then(data => mostrarDetalle(data));

function mostrarDetalle(lista) {

    const pelicula = lista.find(p => p.ID == id);

    if (!pelicula) {
        document.body.innerHTML = "<h1>Película no encontrada</h1>";
        return;
    }

    // Llenar la información
    document.getElementById("titulo").textContent = pelicula.Título;
    document.getElementById("anio").textContent = pelicula.Año;
    document.getElementById("director").textContent = pelicula.Director;
    document.getElementById("sinopsis").textContent = pelicula.Sinopsis;

    // Imagen
    document.getElementById("imagen").src = "/static/img/" + pelicula.Imagen;
    document.getElementById("imagen").alt = pelicula.Título;

    // Trailer
    document.getElementById("trailer").src = pelicula.Trailer;
}
