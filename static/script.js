function sendMessage() {
    let user = document.getElementById("username").value;
    let msg = document.getElementById("msg").value;

    if (!user || !msg) return;

    fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user, message: msg })
    });

    document.getElementById("msg").value = "";
}

let lastMessageCount = 0;

setInterval(() => {
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
            }
        });
}, 1000);


setInterval(() => {
    fetch("/messages")
        .then(res => res.json())
        .then(data => {
            let chat = "";

            data.forEach(m => {
                if (m.type === "audio") {
                    chat += `
                        <audio controls>
                            <source src="/static/audio/${m.file}" type="audio/webm">
                        </audio><br>
                    `;
                } else {
                    chat += `<p><b>${m.user}:</b> ${m.message}</p>`;
                }
            });

            document.getElementById("messages").innerHTML = chat;
        });
}, 1000);

