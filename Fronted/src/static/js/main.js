// JavaScript principal para EIVAI
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Añadir animación fade-in a las cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Manejar formulario de contacto
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleContactForm();
        });
    }

    // Añadir indicador de página activa en la navegación
    setActiveNavItem();
});

/**
 * Manejar el envío del formulario de contacto
 */
function handleContactForm() {
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;
    const privacy = document.getElementById('privacy').checked;

    if (!privacy) {
        showAlert('Por favor, acepta los términos y condiciones de privacidad.', 'warning');
        return;
    }

    // Simular envío de formulario
    showAlert('¡Mensaje enviado correctamente! Te contactaremos pronto.', 'success');
    
    // Limpiar formulario
    document.querySelector('form').reset();
}

/**
 * Mostrar alertas
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insertar alerta al principio del contenido principal
    const main = document.querySelector('main');
    main.insertBefore(alertContainer, main.firstChild);

    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

/**
 * Establecer el item activo en la navegación
 */
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Función para verificar el estado del servidor
 */
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('Estado del servidor:', data);
        return data;
    } catch (error) {
        console.error('Error al verificar el estado del servidor:', error);
        return null;
    }
}

/**
 * Función para smooth scroll
 */
function smoothScroll(target) {
    document.querySelector(target).scrollIntoView({
        behavior: 'smooth'
    });
}
