let textTextarea = document.getElementById("textTextarea");
let sendButton = document.getElementById("sendButton");
let modelTextArea = document.getElementById("modelTextArea");
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
                "model": modelTextArea.value,
                "text": textTextarea.value
            })
        }
    ).then(res => {
        if (!res.ok) {
            if (res.status === 422) {
                throw new Error(`Server got an unprocessable entity (make sure a valid model is selected)`);
            } else if (res.status == 400) {
                throw new Error(`Server got a bad request (make sure text is non-empty and contains valid characters)`);
            } else {
                throw new Error(`Error while sending request to remote server (Status ${res.status}`);
            }
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
