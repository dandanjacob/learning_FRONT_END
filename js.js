async function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (!userInput) return; // Não envia mensagens vazias

    // Adiciona a mensagem do usuário ao chat
    addMessage('Você: ' + userInput);

    // Limpa o campo de entrada
    document.getElementById('user-input').value = '';

    // Envia a mensagem para a API
    const response = await fetch('http://127.0.0.1:8000/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();

    // Adiciona as respostas do bot ao chat
    data.response.forEach((msg) => {
        addMessage('Bot: ' + msg);
    });
}

// Função para adicionar uma mensagem ao chat
function addMessage(text) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);

    // Rola para a última mensagem
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Evento de clique no botão "Enviar"
document.getElementById('send-button').addEventListener('click', sendMessage);

// Evento de pressionar "Enter" no campo de entrada
document.getElementById('user-input').addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});