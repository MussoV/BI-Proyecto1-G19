// Variable global para llevar el conteo de las reseñas
var reviewCount = 0;

// Función para realizar una petición al servidor con un texto
function predictText(event) {
    // Prevenir el comportamiento predeterminado del formulario
    event.preventDefault();

    // Obtener el texto ingresado por el usuario
    var text = document.getElementById('texto').value;

    // Verificar si el campo de texto está vacío o contiene solo espacios en blanco
    if (text.trim() === '') {
        // Mostrar un mensaje de error al usuario
        alert('Por favor, ingresa una reseña antes de predecir.');
        // Detener la ejecución de la función
        return;
    }

    // Objeto con los datos a enviar al servidor
    var data = {
        text: text
    };

    // Realizar la petición POST al servidor
    fetch('/predict_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Incrementar el conteo de las reseñas
        reviewCount++;

        // Crear una nueva fila en la tabla con la reseña y la predicción
        var tableBody = document.querySelector('#reviewTable tbody');
        var newRow = tableBody.insertRow();
        newRow.innerHTML = `
            <td>${reviewCount}</td>
            <td>${text}</td>
            <td>${data.prediction}</td>
        `;
        
        // Limpiar el cuadro de texto
        document.getElementById('texto').value = '';
    })
    .catch(error => console.error('Error:', error));
}

// Función para realizar una petición al servidor con un archivo CSV
function predictCSV() {
    // Obtener el archivo seleccionado por el usuario
    var file = document.getElementById('archivo').files[0];

    // Crear un objeto FormData para enviar el archivo
    var formData = new FormData();
    formData.append('file', file);

    // Realizar la petición POST al servidor
    fetch('/predict_csv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Limpiar la tabla antes de agregar nuevas filas
        var tableBody = document.querySelector('#reviews tbody');
        tableBody.innerHTML = '';

        // Iterar sobre cada reseña en el objeto JSON y agregarla a la tabla
        data.reviews.forEach(review => {
            var newRow = tableBody.insertRow();
            newRow.innerHTML = `
                <td>${review.ID}</td>
                <td>${review.Review}</td>
                <td>${review.prediction}</td>
            `;
        });
    })
    .catch(error => console.error('Error:', error));
}


