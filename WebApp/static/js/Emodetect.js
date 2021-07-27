const s = document.getElementById('EmoDetection');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const uploadWidth = s.getAttribute("data-uploadWidth") || 480; //the width of the upload file
const mirror = s.getAttribute("data-mirror"); //mirror the boundary boxes

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
var div = document.getElementById('myCanvas');
div.appendChild(drawCanvas);

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
 
    //Set canvas sizes based on input video
    drawCanvas.width = v.videoWidth;
    drawCanvas.height = v.videoHeight;
    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (v.videoHeight/v.videoWidth);
    console.log(window.innerWidth, window.innerHeight);
    //Some styles for the drawcanvas
    drawCtx.lineWidth = "4";
    drawCtx.strokeStyle = "blue";
    drawCtx.font = "20px Verdana";
    drawCtx.fillStyle = "yellow";
    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoWidth/v.videoHeight));
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
            //draw the boxes
            drawBoxes(objects);
            //sendImageFromCanvas();
            //Send the next image
            imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, (imageCanvas.clientWidth-v.videoWidth)/4, 0, v.videoWidth, v.videoHeight);
            imageCanvas.toBlob(postFile, 'image/jpeg');
        }
        else{
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

function drawBoxes(object) {
 
    //clear the previous drawings
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    
    //filter out objects that contain a class_name and then draw boxes and labels on each
    
    let x = object.x;
    let y = object.y;
    let width = (object.w) + x;
    let height = (object.h)+ y;
    //flip the x axis if local video is mirrored
    if (mirror){
            x = drawCanvas.width - (x + width)
        }
    //+ Math.round(object.score * 100, 1) + "%"
    drawCtx.fillText(object.class_name, x + 5, y - 70);
    drawCtx.strokeRect(x-100, y-50, width-10, height);
 
    
}

