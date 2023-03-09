console.log("Script loaded.");
const startAttendanceButton = document.getElementById('start-attendance');
const stopAttendanceButton = document.getElementById('stop-attendance');

// Start the camera stream when the Start Attendance button is clicked
startAttendanceButton.addEventListener('click', () => {
  // startCamera();
  console.log("Pressed Start-Attendance Button");
  const ids = '{{ students }}';
  document.getElementById("testjs").innerHTML=ids;
  startAttendanceButton.disabled = true;
  stopAttendanceButton.disabled = false;
});

// Stop the camera stream when the Stop Attendance button is clicked
stopAttendanceButton.addEventListener('click', () => {
  console.log("Pressed Stop-Attendance Button");
  // video.srcObject.getTracks().forEach((track) => {
  //   track.stop();
  // });
  startAttendanceButton.disabled = false;
  stopAttendanceButton.disabled = true;
});