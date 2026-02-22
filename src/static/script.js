let textTextarea = document.getElementById("textTextarea");
let sendButton = document.getElementById("sendButton");
let saveTextArea = document.getElementById("saveTextArea");
saveTextArea.value = "mySound.wav";

sendButton.addEventListener("click", () => {
    let url = window.location.href;
    fetch(
        `${url}api/speak`, 
        {
            "headers": new Headers({"content-type": "application/json"}),
            "method": "POST",
            "body": JSON.stringify({
                "voice": 0,
                "rate": 200,
                "volume": 1.0,
                "text": textTextarea.value
            })
        }
    ).then(res => {
        if (!res.ok) {
            throw new Error(`Error while sending request to remote server (Status ${res.status}`);
        } 

        return res.blob();
    }).then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");

        a.href = url;
        a.download = saveTextArea.value;

        a.click();
        a.remove();
    }).catch(err => {
        alert(err);
    })
});
