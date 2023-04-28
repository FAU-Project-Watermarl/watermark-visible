const express = require('express')
const app = express()
const bodyParser = require('body-parser');
// const fs = require('fs');
const fs = require('fs-extra');
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
    //res.send(__dirname + 'index.html')
    res.send(__dirname, 'index.html')
    //path.join(__dirname, 'index.html')
    // res.send(path.join(__dirname, 'index.html'))
    // res.send(path.join(__dirname, 'index.html'))
});

app.post('/delete-videos',async function (req, res) {
    await deleteFolder()
    res.status(200).json({ message: 'Videos deleted' });
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
        // deleteFolder()
        await executeContainer();
       
       //await 
        //res.redirect('/');
        // fs.readFile
        let extractResult =''
        try {
             extractResult = fs.readFileSync('./public/videos/extract.txt', 'utf8');
            console.log(extractResult);
          } catch (err) {
            console.error(err);
          }
        
        res.status(200).json({ message: extractResult });
        
    })

    //  connect the docker
    // res.status(200);
    // console.log('HERE');
    
})




async function executeContainer() {
    const { execSync } = require("child_process");
    console.log('\n#######################################');
    console.log('Executing python container')
    console.log('#######################################\n');
    execSync("cd Docker && sh operations.sh", (error, stdout, stderr) => {
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



    console.log('\n#######################################');
    console.log('Watermark and Validation process Done');
    console.log('#######################################\n');
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

async function deleteFolder () {
    try {
      await fs.emptyDir('./public/videos')
      console.log('success!')
    } catch (err) {
      console.error(err)
    }
  }

port = process.env.PORT || 3000
var listener = app.listen(port); //start the server
console.log('=========================================')
console.log('||  Server is running on Port: ', port,'  ||');
console.log('=========================================')

