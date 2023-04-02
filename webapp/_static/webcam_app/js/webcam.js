const video = document.getElementById('videoElement');
const canvas = document.getElementById('canvasElement');

function startWebcam() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
      const mediaStreamTrack = stream.getVideoTracks()[0];
      const imageCapture = new ImageCapture(mediaStreamTrack);
      setInterval(() => {
        imageCapture.grabFrame()
          .then(imageBitmap => {
            canvas.width = imageBitmap.width;
            canvas.height = imageBitmap.height;
            const context = canvas.getContext('2d');
            context.drawImage(imageBitmap, 0, 0, canvas.width, canvas.height);
            canvas.toBlob((blob) => {
              const xhr = new XMLHttpRequest();
              xhr.open('POST', '/cam/process_frame/');
              xhr.setRequestHeader('Content-Type', 'image/jpeg ');
              xhr.send(blob);
            }, 'image/jpeg ');
          })
          .catch(error => {
            console.error(error);
          });
      }, 200);
    })
    .catch(error => {
      console.error(error);
    });
}


function stopWebcam() {
  const stream = video.srcObject;
  const tracks = stream.getTracks();
  tracks.forEach(track => track.stop());
  video.srcObject = null;
}

const startButton = document.getElementById('startButton');
startButton.addEventListener('click', () => {
  startWebcam();
});



const stopButton = document.getElementById('stopButton');
stopButton.addEventListener('click', () => {
  stopWebcam();
});
