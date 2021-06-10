var ws = new WebSocket("ws://localhost:8888/websiteWebsocket");
//var username = prompt("What's your name?");

var panSlider = document.getElementById("panRange");
var panVal = document.getElementById("panVal");
panVal.innerHTML = panSlider.value; // Display the default slider value
var tiltSlider = document.getElementById("tiltRange");
var tiltVal = document.getElementById("tiltVal");
tiltVal.innerHTML = tiltSlider.value; // Display the default slider value

var cam1_check = document.getElementById('cam1_check');
var cam2_check = document.getElementById('cam2_check');

// Update the current slider value (each time you drag the slider handle)
panSlider.oninput = function() {
  panVal.innerHTML = this.value;
  sendMessagePan();
}

// Update the current slider value (each time you drag the slider handle)
tiltSlider.oninput = function() {
    panVal.innerHTML = this.value;
    sendMessageTilt();
}

function sendMessagePan() {
    var message = panSlider.value;
    var payload = {
        "type": "servo",
        "dir": "pan",
        "mag": message
    }
    // Make the request to the WebSocket.
    ws.send(JSON.stringify(payload));
    return false;
}

function sendMessageTilt() {
    var message = tiltSlider.value;
    var payload = {
        "type": "servo",
        "dir": "tilt",
        "mag": message
    }
    // Make the request to the WebSocket.
    ws.send(JSON.stringify(payload));
    return false;
}

function sendMessagePic() {
    
    if (cam1_check.checked) {
        var payload = {
            "type": "cap",
            "mode": "single",
            "cam": "1"
        }
        ws.send(JSON.stringify(payload));
    }
    
    if (cam2_check.checked) {
        var payload = {
            "type": "cap",
            "mode": "single",
            "cam": "2"
        }
        ws.send(JSON.stringify(payload));
    }
}

function sendMessagePano() {
    var payload = {
        "type": "cap",
        "mode": "pano",
        "cam": "1"
    }

    ws.send(JSON.stringify(payload));
    return false;
}

ws.onmessage = function(evt) {
    var messageDict = JSON.parse(evt.data);
    // Create a div with the format `user: message`.
    var messageBox = document.createElement("div");
    messageBox.innerHTML = evt.data;
    document.getElementById("messages").appendChild(messageBox);
};