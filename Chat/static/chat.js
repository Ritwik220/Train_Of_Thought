// User is defined and assigned in chat.html
// Variable to store the name of the contact or group the user is sending the message to
let to = null;
let charSocket = null;

document.addEventListener("DOMContentLoaded", () => {
    // Check point
    console.log("Document Loaded");
    // Getting all the contacts present and displaying them for the user
    let contacts = document.querySelectorAll('.contact');
    let contacts_name = document.querySelectorAll('.contact-name');
    let i = 0;
    for(contact of contacts) {
        updateChatUser(contact, contacts_name[i]);
        i++;
    }
    // Check point
    console.log(to);

    // Taking the submit button and assigning an event of sending the message to the backend to it if pressed
    let chat_submit = document.getElementById("send-button");
    chat_submit.addEventListener('click', sendMessage);
    var search = document.getElementById("search");
    // Doing the same if the enter key is pressed
    document.addEventListener('keydown', function(event) {
     if(event.key === 'Enter') {
        sendMessage();
    }
    else if(search.innerHTML !== "null") {
        console.log("Search value: ", search.value);
        searchContact(search.value);
    }
    });


}
)


function searchContact(searchTerm) {
    let contacts = document.querySelectorAll('.contact-name');
    contacts.forEach(contact => {
        console.log("Contact name: ", contact.innerHTML.toLowerCase().substring(0, searchTerm.length));
        console.log("Search term: ", searchTerm);
        if(contact.innerHTML.toLowerCase().includes(searchTerm.toLowerCase())) {
            contact.style.display = 'block';
        } else {
            contact.style.display = 'none';
        }
    });
}

// Displaying the name of the contact selected at the top of the chat area
function updateChatUser(element, name){
    let heading = document.querySelector('.personal-info');
    element.addEventListener('click', () => {
        heading.innerHTML = name.innerHTML;
        to = name.innerHTML;
        createChatRoom(to)
        // console.log(to);
    });
}

// A function which sends a message to the backend.
function sendMessage() {
    if(charSocket != null) {
        let messageInput = document.getElementById("message-input");
        let message = messageInput.value;
        charSocket.send(JSON.stringify({
            'message': message,
            'status': 'received',
            'user': username,
            'to': to,
        }));
        // Resetting the input to null after the message has been sent to the backend.
        messageInput.value = '';
    } else {
        console.error("Chat socket is not connected.");
    }
}

// Creating a chat room.
function createChatRoom(to){
     console.log("Connected to chat with ", to);
     const encodedTo = encodeURIComponent(to);
     let url = `ws://${window.location.host}/ws/socket-server/${encodedTo}/`;
     console.log(url);
     charSocket = new WebSocket(url);
     // Check point
     // charSocket.onopen = () => console.log("WebSocket opened");
     // charSocket.onerror = (e) => console.error("WebSocket error:", e);
     // charSocket.onclose = (e) => console.log("Closed", e);
     // Displaying the message received from the backend in the chat area.
     charSocket.onmessage = function(e) {
         console.log("Message received from the backend:", e.data);
         let data = JSON.parse(e.data);
         console.log("Username: ", username);
         console.log("Other username: ", data.user);
         // console.log(data.email === email && to === data.to);
         if(data.type === 'chat') {
             let chatBox = document.getElementById("chat-messages");
             let messageElement = document.createElement("p");
             if(data.status === 'sent') {
                 messageElement.className = "chat-message sent";
                 console.log("Message sent by user:", data.user);
             } else {
                 messageElement.className = "chat-message received";
                 console.log("Message received from user:", data.user);
             }
             if (data.message != null && data.message.trim() !== "") {
                  let commenter = data.user + ": ";
                  if(data.user === username) {
                     commenter = "";
                 }
                 messageElement.textContent = commenter + "\n" + data.message;
                 chatBox.appendChild(messageElement);
                 chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
             }
             }
         else if(data.type==='connection_established'){
             let chatBox = document.getElementById("chat-messages");
             chatBox.innerHTML = ""; // Clear previous messages
             data.past.forEach(chat => {
                 let sender = chat.by + ": ";
                 let messageElement = document.createElement("p");
                 let status = "received";
                 console.log("Adding previous msgs ", data.past.by === username)
                 console.log(data.past);
                 console.log(chat.by, username);
                 if(chat.by === username.replace("%20", " ")) {
                     status = "sent";
                     sender = "";
                 }
                 messageElement.className = "chat-message " + status;
                 messageElement.textContent = sender + chat.message;
                 chatBox.appendChild(messageElement);
                 chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
             });
         }
         else {
             console.error("Unknown data type received:", data.type);
         }
     };
}
