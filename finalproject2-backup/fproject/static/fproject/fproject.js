function loadchat(username) {
    fetch(`http://127.0.0.1:8000/json_chat/${username}`)
    .then(response => response.json())
    .then(chats => {
        document.querySelector('#chatbox').innerHTML = '';
        chats.forEach(chat => {
            let row = document.createElement('div');
            row.className = "row mb-2";
            let col = document.createElement('div');
            if (chat.message_sender != username) {
                col.className = "col-md-4 border";
            } else {
                col.className = "col-md-4 offset-md-8 border";
            }
            col.innerHTML = `${chat.message} <br> <p class="text-right text-muted small">${chat.date}</p>`;
            row.append(col);
            document.querySelector('#chatbox').append(row);
        })
    })
}