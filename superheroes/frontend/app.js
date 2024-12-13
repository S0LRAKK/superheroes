const API_URL = "http://127.0.0.1:8000";

// Maneja el formulario de agregar un personaje
document.getElementById("item-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const alias = document.getElementById("alias").value;
    const nombre = document.getElementById("nombre").value;
    const edad = document.getElementById("edad").value;

    const response = await fetch(`${API_URL}/personajes/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ alias, nombre, edad: parseInt(edad) }),
    });

    if (response.ok) {
        loadItems();
    } else {
        console.error("Error al agregar un personaje");
    }
});

// Función para cargar los personajes
async function loadItems() {
    try {
        const response = await fetch(`${API_URL}/personajes/`);
        if (!response.ok) {
            throw new Error("Error al buscar personajes");
        }
        const personajes = await response.json();
        const list = document.getElementById("items-list");
        list.innerHTML = "";
        personajes.forEach((personaje) => {
            const li = document.createElement("li");
            li.textContent = `${personaje.alias} (${personaje.nombre}), Edad: ${personaje.edad}`;
            list.appendChild(li);
        });
    } catch (error) {
        console.error(error.message);
    }
}

loadItems();
