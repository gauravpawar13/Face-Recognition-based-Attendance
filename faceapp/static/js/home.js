const canvas = document.getElementById('camera-canvas');
const context = canvas.getContext('2d');
const video = document.createElement('video');
video.autoplay = true;

// Start the camera stream and display the video stream in the canvas element
function startCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
      video.addEventListener('loadedmetadata', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        requestAnimationFrame(drawVideo);
      });
    })
    .catch((error) => {
      console.error('Error accessing camera:', error);
    });
}

// Draw the video stream in the canvas element
function drawVideo() {
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  requestAnimationFrame(drawVideo);
}
const startAttendanceButton = document.getElementById('start-attendance-button');
const stopAttendanceButton = document.getElementById('stop-attendance-button');

// Start the camera stream when the Start Attendance button is clicked
startAttendanceButton.addEventListener('click', () => {
  startCamera();
  startAttendanceButton.disabled = true;
  stopAttendanceButton.disabled = false;
});

// Stop the camera stream when the Stop Attendance button is clicked
stopAttendanceButton.addEventListener('click', () => {
  video.srcObject.getTracks().forEach((track) => {
    track.stop();
  });
  startAttendanceButton.disabled = false;
  stopAttendanceButton.disabled = true;
});
