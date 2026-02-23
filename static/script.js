let mediaRecorder;
let audioChunks = [];
let isRecording = false;

async function startRecording() {
    if (!isRecording) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };

        mediaRecorder.onstop = sendAudio;

        mediaRecorder.start();
        isRecording = true;
        document.getElementById("recordBtn").innerText = "⏹️";
    } else {
        mediaRecorder.stop();
        isRecording = false;
        document.getElementById("recordBtn").innerText = "🎤";
    }
}

function sendAudio() {
    const blob = new Blob(audioChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", blob);

    fetch("/upload_audio", {
        method: "POST",
        body: formData
    });
}


function sendMessage() {
    let msg = document.getElementById("msg").value.trim();
    if (!msg) return;

    fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user: username,
            message: msg
        })
    });

    document.getElementById("msg").value = "";
}

let lastMessageCount = 0;

function fetchMessages() {
    fetch("/messages")
        .then(res => res.json())
        .then(data => {

            if (data.length > lastMessageCount) {
                let chatBox = document.getElementById("messages");

                for (let i = lastMessageCount; i < data.length; i++) {
                    let m = data[i];

                    if (m.type === "audio") {
                        let audio = document.createElement("audio");
                        audio.controls = true;
                        audio.src = "/static/audio/" + m.file;
                        chatBox.appendChild(audio);
                        chatBox.appendChild(document.createElement("br"));
                    } else {
                        let p = document.createElement("p");
                        p.innerHTML = `<b>${m.user}:</b> ${m.message}`;
                        chatBox.appendChild(p);
                    }
                }

                lastMessageCount = data.length;

                chatBox.scrollTop = chatBox.scrollHeight;
            }
        });
}
setInterval(fetchMessages, 1000);