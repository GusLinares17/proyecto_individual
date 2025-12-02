fetch("../../peliculas.json")
    .then(response => response.json())
    .then(data => mostrarPeliculas(data));

function mostrarPeliculas(lista) {
    const contenedor = document.getElementById("lista-peliculas");

    lista.forEach(peli => {
        const tarjeta = document.createElement("div");
        tarjeta.classList.add("card-pelicula");

        tarjeta.innerHTML = `
            <img src="../img/${peli.Imagen}" alt="${peli.Título}">
            <h3>${peli.Título}</h3>
            <button onclick="verDetalle(${peli.ID})">Ver más</button>
        `;

        contenedor.appendChild(tarjeta);
    });
}

function verDetalle(id) {
    window.location.href = `detalle.html?id=${id}`;
}
