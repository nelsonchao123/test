// load the things we need
var express = require('express');
var app = express();
const axios = require("axios")

// set the view engine to ejs
app.set('view engine', 'ejs');

app.get('/', function(req, res) {

    var arr = [];
    while(arr.length < 3)
    {
        var a = Math.floor(Math.random() * 10) + 1;
        if(arr.indexOf(a) === -1) arr.push(a);
    }

    axios.get("https://jsonplaceholder.typicode.com/users/")
    .then((response)=>{
        let users = [
            {namE: response.data[arr[0]-1].name, citY: response.data[arr[0]-1].address.city, comP: response.data[arr[0]-1].company.name},
            {namE: response.data[arr[1]-1].name, citY: response.data[arr[1]-1].address.city, comP: response.data[arr[1]-1].company.name},
            {namE: response.data[arr[2]-1].name, citY: response.data[arr[2]-1].address.city, comP: response.data[arr[2]-1].company.name}
        ];

        res.render('pages/index', {
            users: users
        });
    })

        

});

app.listen(8080);
console.log('8080 is the magic port');
