// static/js/hand-control.js
// Use the global 'socket' variable declared in index.html

// Assume you have access to the 3D model or object from viewer.js
// We'll export model from viewer.js and import it here (or pass via global scope)

socket.on("gesture", (data) => {
    console.log("Gesture data:", data);

    if (window.model) {
        window.model.rotation.x += data.rotateX * 0.01;
        window.model.rotation.y += data.rotateY * 0.01;
    }
});

// (Optional) Render hand landmarks in 3D if needed
socket.on("landmarks", (points) => {
    if (window.handLandmarks) {
        for (let i = 0; i < window.handLandmarks.length; i++) {
            window.handLandmarks[i].position.set(points[i][0] * 5 - 2.5, -points[i][1] * 5 + 2.5, -points[i][2] * 5);
        }
    }
});
