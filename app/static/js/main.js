/**
 * JavaScript principal para Hoodie Shop
 * Funcionalidades del lado del cliente
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Validación de formularios de Bootstrap
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Confirmación de contraseñas en registro
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    
    if (passwordField && confirmPasswordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordField.setCustomValidity('Las contraseñas no coinciden');
            } else {
                confirmPasswordField.setCustomValidity('');
            }
        });
    }
    
    // Formatear precios mientras el usuario escribe
    const precioInputs = document.querySelectorAll('input[name="precio"]');
    precioInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = Math.round(value);
            }
        });
    });
    
    // Preview de imagen antes de subir
    const imagenInput = document.getElementById('imagen');
    if (imagenInput) {
        imagenInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    // Crear o actualizar preview
                    let preview = document.getElementById('image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'image-preview';
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        imagenInput.parentNode.appendChild(preview);
                    }
                    preview.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Actualizar subtotales en carrito al cambiar cantidades
    const cantidadInputs = document.querySelectorAll('input[name^="cantidad_"]');
    cantidadInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Aquí podrías agregar lógica para calcular subtotales dinámicamente
            // Por ahora, el formulario se envía para recalcular en el servidor
            console.log('Cantidad cambiada:', this.value);
        });
    });
    
    // Tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popovers de Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    console.log('✅ Hoodie Shop JS cargado correctamente');
});

/**
 * Función para formatear números como moneda COP
 */
function formatearCOP(numero) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(numero);
}

/**
 * Función para confirmar eliminación
 */
function confirmarEliminacion(mensaje) {
    return confirm(mensaje || '¿Estás seguro de eliminar este elemento?');
}