const constraints = {
    audio: false,
    video: {
        width: {min: 480, ideal: 720, max: 1080},
        height: {min: 480, ideal: 720, max: 1080}
    }
};

navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        document.getElementById("myVideo").srcObject = stream;
        console.log("Got local user video");
 
    })
    .catch(err => {
        console.log('navigator.getUserMedia error: ', err)
    });