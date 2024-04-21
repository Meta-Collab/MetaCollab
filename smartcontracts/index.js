const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;
app.use(express.json());
const { push, new_room, get_commits }= require('./scripts/interact.js');
const { upload }= require('./scripts/pinata.js');

const API = axios.create({
    baseURL: 'http://localhost:8000',
});

app.post('/new_room', async (req, res) => {
    const room_id = req.body.room_id;
    const members=req.body.members;
    try {
        const result = await new_room(room_id, members);
        res.send('Success!');
    } catch (error) {
        console.error(error);
    }
});

app.post('/get_commits',async (req, res) => {
    const room_id=req.body.room_id;
    console.log(room_id);
    try {
        console.log("check",await get_commits(room_id));
        res.json({ commits });
        //res.send('Success!');
    } catch (error) {
        console.error(error);
    }
});

app.post('/upload_file', async (req, res) => {
    const file_path = req.body.file_path;
    const room_id=req.body.room_id;
    try {
        const url = await upload(file_path,room_id);
        //res.send('Success!');
        res.json({url});
    } catch (error) {
        console.error(error);
    }
});


app.post('/put_string', async (req, res) => {
    const complete_string = req.body.complete_string;
    const roomuuid=req.body.roomuuid;
    // try {
    //     const url = await main(file_path);
    //     API.post('/api/get_file_url', { url: url })
    //         .then(response => {
    //             res.send('Success!');
    //         })
    //     res.send('Success!');
    // } catch (error) {
    //     console.error(error);
    // }
    try {
        const result = await push(complete_string, roomuuid);
        res.send('Success!');
    } catch (error) {
        console.error(error);
    }
});
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});