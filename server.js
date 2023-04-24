const express = require('express')
const app = express()
const bodyParser = require('body-parser');
const fs = require('fs');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }))
app.use(express.static('./public'));

app.get('/', (req, res)=> {
    res.send(__dirname+'index.html')
});

port = process.env.PORT || 3000
var listener = app.listen(port); //start the server
console.log('Server is running on Port: ',port);

