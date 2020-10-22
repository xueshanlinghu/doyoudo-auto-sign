const express = require('express');
const app = express();

app.get('/', function(req, res){
    res.send('Hello world');
});

var server = app.listen(3002, function() {
    console.log('Listening on port %d', server.address().port);
})