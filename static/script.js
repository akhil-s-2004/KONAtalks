function selectVillain() {
    const villainSelect = document.getElementById("villain-select");
    const selectedVillain = villainSelect.value;

    if (!selectedVillain) {
        addMessage("Please select a villain to start chatting.", "bot-message");
        return;
    }

    fetch('/konatalks/select_villain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ villain: selectedVillain })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            addMessage(data.error, "bot-message");
        } else {
            addMessage(data.message, "bot-message");
            // Call addImage to display the villain's image
            addImage(data.image);
            document.getElementById("user-input").disabled = false;
            document.querySelector(".chat-input button").disabled = false;
        }
    })
    .catch(error => {
        addMessage("Oops! Something went wrong while selecting the villain.", "bot-message");
    });
}

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const messageText = userInput.value.trim();
    
    if (messageText === "") return;

    addMessage(messageText, "user-message");

    fetch('/konatalks/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            addMessage(data.error, "bot-message");
        } else {
            addMessage(data.message, "bot-message");
        }
    })
    .catch(error => {
        addMessage("Oops! Something went wrong while sending your message.", "bot-message");
    });

    userInput.value = "";
}

function addImage(imageUrl) {
    const chatBox = document.getElementById("chat-box");

    const imageDiv = document.createElement("div");
    imageDiv.classList.add("message", "bot-message"); // Add class for styling

    const imageElement = document.createElement("img");
    imageElement.src = imageUrl;
    imageElement.alt = "Villain Image";
    imageElement.classList.add("villain-image"); // Add class for styling if needed

    imageDiv.appendChild(imageElement);
    chatBox.appendChild(imageDiv);
    
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom of the chat
}

function addMessage(text, className) {
    const chatBox = document.getElementById("chat-box");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", className);

    const messageSpan = document.createElement("span");
    messageSpan.textContent = text;

    messageDiv.appendChild(messageSpan);
    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom of the chat
}

// Optional: For better user experience, add an event listener for the Enter key
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
