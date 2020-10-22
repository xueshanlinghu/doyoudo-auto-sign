var CryptoJS = require("crypto-js");

var key = "dyd"     //秘钥必须为：8/16/32位
var message = "36977f9e-41b0-49dd-b293-d059a79bbb36";

//加密
var encrypt = CryptoJS.AES.encrypt(message, key, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
});
console.log("value: "+encrypt);

//解密
var decrypt = CryptoJS.AES.decrypt(encrypt, key, {
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
});
console.log("value: "+decrypt.toString(CryptoJS.enc.Utf8));