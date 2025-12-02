const params = new URLSearchParams(window.location.search);
const id = params.get("id");

fetch("../../peliculas.json")
    .then(response => response.json())
    .then(data => mostrarDetalle(data));

function mostrarDetalle(lista) {
    const pelicula = lista.find(p => p.ID == id);

    if (!pelicula) {
        document.body.innerHTML = "<h1>Película no encontrada</h1>";
        return;
    }

    document.getElementById("titulo").textContent = pelicula.Título;
    document.getElementById("anio").textContent = pelicula.Año;
    document.getElementById("director").textContent = pelicula.Director;
    document.getElementById("sinopsis").textContent = pelicula.Sinopsis;

    document.getElementById("imagen").src = "../img/" + pelicula.Imagen;
    document.getElementById("imagen").alt = pelicula.Título;

    document.getElementById("trailer").src = pelicula.Trailer;
}
