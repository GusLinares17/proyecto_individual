// Cargar JSON con las películas
fetch("/peliculas.json")
    .then(res => res.json())
    .then(data => mostrarPeliculas(data));

function mostrarPeliculas(lista) {

    const contenedor = document.getElementById("lista-peliculas");

    lista.forEach(peli => {

        const tarjeta = document.createElement("div");
        tarjeta.classList.add("card-pelicula");

        tarjeta.innerHTML = `
            <img src="/static/img/${peli.Imagen}" alt="${peli.Título}">
            <h3>${peli.Título}</h3>
            <button onclick="verDetalle(${peli.ID})">Ver más</button>
        `;

        contenedor.appendChild(tarjeta);
    });
}

function verDetalle(id) {
    window.location.href = `/static/detalle.html?id=${id}`;
}

