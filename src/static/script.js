let textTextarea = document.getElementById("textTextarea");
let sendButton = document.getElementById("sendButton");
let modelDropDown = document.getElementById("modelDropDown");
let saveTextArea = document.getElementById("saveTextArea");

const url = window.location.href;
saveTextArea.value = "mySound.wav";

fetch(`${url}api/models`)
.then(res => {
    if (!res.ok)
        throw new Error("Response from remote server was not ok. Make sure it is running.");

    return res.json()
}).then(parsedJson => {
    for (let e of parsedJson) {
        let option = document.createElement("option");
        option.value = e;
        option.text = e;
        modelDropDown.add(option)
    }
}).catch(err => {
    alert(err)
});

sendButton.addEventListener("click", () => {
    fetch(
        `${url}api/speak`, 
        {
            "headers": new Headers({"content-type": "application/json"}),
            "method": "POST",
            "body": JSON.stringify({
                "model": modelDropDown.value,
                "text": textTextarea.value
            })
        }
    ).then(res => {
        if (!res.ok) {
            if (res.status === 422) 
                throw new Error(`Server got an unprocessable entity (make sure a valid model is selected)`);
            else if (res.status === 400) 
                throw new Error(`Server got a bad request (make sure text is non-empty and contains valid characters)`);
            else 
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
