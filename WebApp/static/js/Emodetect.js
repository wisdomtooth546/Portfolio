const s = document.getElementById('EmoDetection');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const uploadWidth = s.getAttribute("data-uploadWidth") || 480; //the width of the upload file
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes

v = document.getElementById(sourceVideo);
 
//for starting events
let isPlaying = false,
    gotMetadata = false;
 
//Canvas setup
 
//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");
 
//create a canvas for drawing object boundaries
let drawCanvas = document.createElement('canvas');
document.body.appendChild(drawCanvas);
let drawCtx = drawCanvas.getContext("2d");

v.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if (isPlaying)
        startObjectDetection();
};
 
//see if the video has started playing
v.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if (gotMetadata) {
        startObjectDetection();
    }
};

function startObjectDetection() {
 
    console.log("starting object detection");
 
    //Set canvas sizes base don input video
    drawCanvas.width = v.videoWidth;
    drawCanvas.height = v.videoHeight;
 
    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (v.videoHeight / v.videoWidth);
 
    //Some styles for the drawcanvas
    drawCtx.lineWidth = "4";
    drawCtx.strokeStyle = "cyan";
    drawCtx.font = "20px Verdana";
    drawCtx.fillStyle = "white";
    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
    imageCanvas.toBlob(postFile, 'image/jpeg');
 
}

function postFile(file) {
 
    //Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);
     
    let xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.origin + '/image', true);
    xhr.onload = function () {
        if (this.status === 200) {
            let objects = JSON.parse(this.response);
            //console.log(objects);
 
            //draw the boxes
            drawBoxes(objects);
            
            //Send the next image
            imageCanvas.toBlob(postFile, 'image/jpeg');
        }
        else{
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

function drawBoxes(objects) {
 
    //clear the previous drawings
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
 
    //filter out objects that contain a class_name and then draw boxes and labels on each
    let x = object.x * drawCanvas.width;
    let y = object.y * drawCanvas.height;
    let width = (object.w * drawCanvas.width) + x;
    let height = (object.h * drawCanvas.height) + y;
 
    //flip the x axis if local video is mirrored
    if (mirror){
            x = drawCanvas.width - (x + width)
        }
 
    drawCtx.fillText(object.class_name + " - " + Math.round(object.score * 100, 1) + "%", x + 5, y + 20);
    drawCtx.strokeRect(x, y, width, height);
 
    
}