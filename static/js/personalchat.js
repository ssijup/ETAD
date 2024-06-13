const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

console.log('id :',id , typeof(id), 'message_username :', message_username, 'receiver:' , receiver)
 
const socket = new WebSocket(
    'ws://'
    + window.location.host 
    + '/ws/chat/'
    + id
    + '/'
);


document.querySelector('#chat-message-submit').onclick = function(e){ 
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'receiver':receiver
    }));

    message_input.value = '';
}

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST", e);
}

socket.onerror = function(e){
    console.log("ERROR OCCURED", e);
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data)
    console.log('data',data);
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `<li class="clearfix">
        <div class="message-data text-right">
          <span class="message-data-time"></span>
          <img
            src="https://bootdey.com/img/Content/avatar/avatar7.png"
            alt="avatar"
          />
        </div>
        <div class="message other-message float-right">
          ${data.message}
        </div>
      </li>`
    }else{
        document.querySelector('#chat-body').innerHTML += `<li class="clearfix">
        <div class="message-data text-right">
          <span class="message-data-time"></span>
          <img
            src="https://bootdey.com/img/Content/avatar/avatar7.png"
            alt="avatar"
          />
        </div>
        <div class="message other-message float-left">
        ${data.message}
        </div>
      </li>`
    }
}

