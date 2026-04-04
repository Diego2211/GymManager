function copiarCodigo(codigo, boton) {
    navigator.clipboard.writeText(codigo)
        .then(() => {
            boton.innerText = "Copiado ✔";
            
            setTimeout(() => {
                boton.innerText = "Copiar";
            }, 2000);
        })
        .catch(err => {
            console.error("Error al copiar:", err);
        });
}

function agregarHorario() {
    const totalForms = document.getElementById('id_horario_set-TOTAL_FORMS');
    const currentCount = parseInt(totalForms.value);

    const container = document.getElementById('horarios');
    const firstForm = container.children[0].cloneNode(true);

    let html = firstForm.innerHTML.replace(/-0-/g, `-${currentCount}-`);
    firstForm.innerHTML = html;

    container.appendChild(firstForm);
    totalForms.value = currentCount + 1;
}