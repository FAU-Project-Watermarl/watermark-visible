const express = require('express')
const app = express()
const bodyParser = require('body-parser');
const fs = require('fs');
const fileUpload = require('express-fileupload')

const path = require('path');

const cors = require('cors');
app.use(cors());

var cp = require('cp')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }))
app.use(express.static('./public'));
app.use(fileUpload())

app.get('/', (req, res) => {
    res.send(__dirname + 'index.html')
});

app.post('/upload-video', async function (req, res) {

    if (!req.files || Object.keys(req.files).length === 0) {
        return res.status(400).json({ message: 'No files were uploaded.' });
    }

    let myFile = req.files.myFile;

    await myFile.mv('./public/videos/input.mp4', async (err) => {
        if (err) {
            return res.status(500).json({ message: err });
        }

        //res.json({ message: 'File uploaded!' });
        cp.sync('./public/videos/input.mp4', './Docker/app/input.mp4')
        await x();
       //res.status(200)
       //await 
    });

    //  connect the docker
    res.redirect('/');
    
})


async function x() {
    const { exec } = require("child_process");

    exec("cd Docker && sh operations.sh", (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });


    // const { spawn } = require("child_process");

    // const ls = spawn("ls", ["-la"]);

    // ls.stdout.on("data", data => {
    //     console.log(`stdout: ${data}`);
    // });

    // ls.stderr.on("data", data => {
    //     console.log(`stderr: ${data}`);
    // });

    // ls.on('error', (error) => {
    //     console.log(`error: ${error.message}`);
    // });

    // ls.on("close", code => {
    //     console.log(`child process exited with code ${code}`);
    // });

}

port = process.env.PORT || 3000
var listener = app.listen(port); //start the server
console.log('Server is running on Port: ', port);

