// 1️⃣ Grundgerüst & Variablen
const chat = document.getElementById('chat');
const pdfUpload = document.getElementById('pdfUpload');
const pdfListDiv = document.getElementById('pdfList');

// Beim Laden der Seite PDF-Liste aktualisieren
window.onload = async () => {
    await updatePDFList();
};

// 2️⃣ Funktion: PDF-Liste aktualisieren
async function updatePDFList() {
    const res = await fetch('/documents'); // API Endpoint
    const data = await res.json();

    if (data.length === 0) {
        pdfListDiv.innerHTML = "<i>Keine PDFs hochgeladen</i>";
        return;
    }

    let html = "<ul>";
    data.forEach(pdf => {
        html += `<li>${pdf.filename} (${pdf.pages} Seiten)</li>`;
    });
    html += "</ul>";
    pdfListDiv.innerHTML = html;
}

// 3️⃣ Funktion: PDFs hochladen
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

    await updatePDFList();
}

// 4️⃣ Funktion: Chat-Frage stellen
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

    if (data.answers.length === 0) {
        addMessage("Keine passenden Antworten gefunden.", 'bot');
        return;
    }

    // Antworten nach PDF gruppieren
    const grouped = {};
    data.answers.forEach(ans => {
        if (!grouped[ans.pdf]) grouped[ans.pdf] = [];
        grouped[ans.pdf].push(ans);
    });

    for (let pdf in grouped) {
        let html = `<b>${pdf}</b>:<br>`;
        grouped[pdf].forEach(ans => {
            html += `Seite ${ans.page} | Score: ${ans.score.toFixed(2)}<br>`;
            html += `<i>${ans.context}</i><br><br>`;
        });
        addMessageHTML(html, 'bot');
    }
}

// 5️⃣ Hilfsfunktionen für Chat
function addMessage(msg, sender) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.textContent = msg;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function addMessageHTML(html, sender) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.innerHTML = html;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}
