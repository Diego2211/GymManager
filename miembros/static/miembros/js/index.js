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