const express = require('express');
const app = express();
const CryptoJS = require("crypto-js");

app.use(express.json()) // for parsing application/json
//app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

function aes_encrypt(text, key) {
    var encrypt = CryptoJS.AES.encrypt(text, key).toString();
    return encrypt
};

app.post("/aes-encrypt", function(req, res){
    console.log(req.body);
    var text = req.body.text;
    var key = req.body.key;
    var result = aes_encrypt(text, key);
    console.log(result)
	res.send(result);
});

var server = app.listen(3002, function() {
    console.log('Listening on port %d', server.address().port);
})