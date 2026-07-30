const API = "http://127.0.0.1:8000";

let uploadedFiles = [];

// =========================
// Upload PDF
// =========================
async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");
    const uploadStatus = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        alert("Please select a PDF.");
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    uploadStatus.style.color = "#555";
    uploadStatus.innerHTML = "⏳ Uploading PDF...";

    try {

        const response = await fetch(`${API}/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Upload Failed");
        }

        const data = await response.json();

        // Prevent duplicate filenames in the list
        if (!uploadedFiles.includes(data.filename)) {
            uploadedFiles.push(data.filename);
        }

        uploadStatus.style.color = "green";

        uploadStatus.innerHTML = `
            <b>✅ Uploaded PDFs</b><br><br>
            ${uploadedFiles.map(f => `📄 ${f}`).join("<br>")}
        `;

    } catch (err) {

        console.error(err);

        uploadStatus.style.color = "red";
        uploadStatus.innerHTML = "❌ Upload Failed";

    }

    fileInput.value = "";
}

// =========================
// Ask Question
// =========================
async function askQuestion() {

    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();

    if (question === "") {
        alert("Please enter a question.");
        return;
    }

    const answerDiv = document.getElementById("answer");

    // Latest chat at the top
    answerDiv.innerHTML = `
        <div class="user">
            👤 <b>You:</b><br><br>
            ${question}
        </div>

        <div class="ai thinking">
            🤖 Thinking...
        </div>

        <hr>
    ` + answerDiv.innerHTML;

    answerDiv.scrollTop = 0;

    try {

        const response = await fetch(`${API}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("Chat Failed");
        }

        const data = await response.json();

        const thinking = document.querySelector(".thinking");

        thinking.classList.remove("thinking");

        let sourcesHTML = "";

        if (data.sources && data.sources.length > 0) {

            sourcesHTML = `
                <br><br>
                <b>📄 Sources</b><br>
                ${data.sources.map(s => `• ${s}`).join("<br>")}
            `;

        }

        let badge = "";

        if (!data.gemini) {
            badge = `
                <div style="
                    background:#fff3cd;
                    color:#856404;
                    padding:10px;
                    border-radius:8px;
                    margin-bottom:15px;
                    border:1px solid #ffeeba;
                ">
                    ⚠️ Gemini API quota exceeded.
                    Showing retrieved document content instead.
                </div>
            `;
        }

    thinking.innerHTML = `
    ${badge}

    🤖 <b>AI:</b><br><br>

    ${data.answer}

    ${sourcesHTML}
    `;

    } catch (err) {

        console.error(err);

        const thinking = document.querySelector(".thinking");

        if (thinking) {
            thinking.classList.remove("thinking");
            thinking.innerHTML = "❌ Unable to get response.";
        }

    }

    questionInput.value = "";
}