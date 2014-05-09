var express = require('express');
var ar_drone = require('ar-drone');

// Create Client
var drone_client = ar_drone.createClient();
drone_client.disableEmergency();
drone_client.on('navdata', console.log);

// Connect to image stream
var pngStream = drone_client.getPngStream();
var lastPng;
pngStream
    .on('error', console.log)
    .on('data', function (pngBuffer) {
        lastPng = pngBuffer;
    });


var app = express();

app.get('/image', function (req, res) {
    if (!lastPng) {
        res.send(503, 'No images received!');
        return;
    }
    res.writeHead(200, {'Content-Type': 'image/png'});
    res.end(lastPng);
});

app.get('/move/:direction', function (req, res) {
    var direction = req.params.direction;
    var valid_directions = ['up', 'down', 'left', 'right', 'front', 'back'];

    if (valid_directions.indexOf(direction) < 0) {
        res.send(400, 'Invalid Direction');
        console.log('Invalid direction received: ' + direction);
    } else {
        if(direction == 'up') {
            drone_client.up(0.2);
            drone_client.after(100, function() {
                this.stop();
            })
        } else if (direction == 'down') {
            drone_client.down(0.2);
            drone_client.after(100, function() {
                this.stop();
            })

        } else  if (direction == 'left') {
            drone_client.left(0.2);
            drone_client.after(100, function() {
                this.stop();
            })

        } else  if (direction == 'right') {
            drone_client.right(0.2);
            drone_client.after(100, function() {
                this.stop();
            })

        } else  if (direction == 'front') {
            drone_client.up(0.2);
            drone_client.after(100, function() {
                this.stop();
            })
        } else  if (direction == 'back') {
            drone_client.up(0.2);
            drone_client.after(100, function() {
                this.stop();
            })
        }
    }
});

app.get('/rotate/:direction', function (req, res) {
    var direction = req.params.direction;
    var valid_directions = ['clockwise', 'anticlockwise'];

    if (valid_directions.indexOf(direction) < 0) {
        res.send(400, 'Invalid Direction');
        console.log('Invalid direction received: ' + direction);
    } else {
        if(direction == 'clockwise') {
            drone_client.up(0.2);
            drone_client.after(100, function() {
                this.stop();
            })
        } else if (direction == 'anticlockwise') {
            drone_client.down(0.2);
            drone_client.after(100, function() {
                this.stop();
            })
        }
    }
});

app.get('/takeoff', function (req, res) {
    drone_client.takeoff();
    res.send('success');
});

app.get('/land', function (req, res) {
    drone_client.land();
    res.end('success');
});

app.listen(3000);