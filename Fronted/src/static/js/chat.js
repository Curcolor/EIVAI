function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return false;
    const messages = document.getElementById('chat-messages');
    // Agrega mensaje del usuario
    messages.innerHTML += `<div class='message sent'><div class='message-content'>${msg}</div></div>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;
    // Simula respuesta automática
    setTimeout(() => {
        messages.innerHTML += `<div class='message received'><div class='message-content'>Simulación: Recibido "${msg}"</div></div>`;
        messages.scrollTop = messages.scrollHeight;
    }, 900);
    return false;
}
