const chat = document.getElementById('chat');
const pdfUpload = document.getElementById('pdfUpload');

async function uploadPDFs() {
    const files = pdfUpload.files;
    if (files.length === 0) return alert("Bitte PDFs auswählen");

    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch('/upload', { method: 'POST', body: formData });
        const data = await res.json();
        addMessage(`Uploaded: ${data.message} (${data.pages} Seiten)`, 'bot');
    }
}

async function askQuestion() {
    const question = document.getElementById('question').value;
    if (!question) return;

    addMessage(question, 'user');

    const formData = new FormData();
    formData.append('question', question);

    const res = await fetch('/ask', { method: 'POST', body: formData });
    const data = await res.json();

    if (data.error) {
        addMessage(data.error, 'bot');
        return;
    }

    for (let ans of data.answers) {
        addMessage(`PDF: ${ans.pdf} | Seite: ${ans.page}\n${ans.context}`, 'bot');
    }
}

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}
