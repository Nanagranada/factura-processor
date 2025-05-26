// Funcionalidad JavaScript para la aplicación

document.addEventListener('DOMContentLoaded', function() {
    // Cerrar automáticamente las alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });

    // Previsualización de archivos PDF
    const invoiceInput = document.getElementById('invoice');
    if (invoiceInput) {
        invoiceInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0].name;
            const fileSize = (e.target.files[0].size / 1024).toFixed(2);
            
            const fileInfo = document.createElement('div');
            fileInfo.className = 'alert alert-success mt-2';
            fileInfo.innerHTML = `<strong>Archivo seleccionado:</strong> ${fileName} (${fileSize} KB)`;
            
            const existingInfo = invoiceInput.parentElement.querySelector('.alert');
            if (existingInfo) {
                existingInfo.remove();
            }
            
            invoiceInput.parentElement.appendChild(fileInfo);
        });
    }

    // Confirmación para eliminar elementos
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
});
