document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const output = document.getElementById('game-output');
    const input = document.getElementById('user-input');
    const prompt = document.getElementById('prompt');

    function scrollToBottom() {
        output.scrollTop = output.scrollHeight;
    }

    socket.on('output', (data) => {
        output.textContent += data;
        scrollToBottom();
    });

    socket.on('input_request', (promptText) => {
        prompt.textContent = promptText;
        input.disabled = false;
        input.focus();
    });

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const value = input.value.trim();
            if (value) {
                output.textContent += prompt.textContent + value + '\n';
                socket.emit('input', value);
                input.value = '';
                scrollToBottom();
            }
        }
    });

    socket.on('disconnect', () => {
        output.textContent += '\n\nConnection lost. Please refresh the page.\n';
        input.disabled = true;
    });
});