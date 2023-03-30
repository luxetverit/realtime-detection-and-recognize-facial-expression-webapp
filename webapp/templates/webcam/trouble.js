const video = document.getElementById('video');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');

let socket;

function setupWebSocket() {
    socket = new WebSocket('ws://' + window.location.host + '/ws/video/');


    socket.onopen = function(event) {
        console.log('WebSocket opened:', event);
  };

    socket.onmessage = function (event) {
        const imageBase64 = event.data;
        video.src = 'data:image/jpeg;base64,' + imageBase64;
};

    socket.onclose = function (event) {
        console.log('WebSocket closed:', event);
};
}
setupWebSocket();


startBtn.addEventListener('click', () => {
if (!socket || socket.readyState === WebSocket.CLOSED) {
  setupWebSocket();
}
socket.send('start');
});

stopBtn.addEventListener('click', () => {
socket.send('stop');
socket.close();

});


window.onbeforeunload = function() {
socket.send('stop');
socket.close();
};
