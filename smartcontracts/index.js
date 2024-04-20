const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;
app.use(express.json());
const { push, new_room, get_commits }= require('./scripts/interact.js');
const { main }= require('./scripts/pinata.js');

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
        const commits=await get_commits(room_id);
        res.json({ commits });
    }catch (error) {
        console.error(error);
    }
});
<<<<<<< HEAD
app.post('/get_commits', (req, res) => {
    const room_id=req.body.room_id;
    commits=get_commits(room_id);
    API.post('/api/list_rooms', { commits: commits })
        .then(response => {
            res.send('Success!');
        }
    )
});
app.post('/take_file)', async (req, res) => {
=======

app.post('/take_file', async (req, res) => {
>>>>>>> 5fffe3fa207e9dc84246da57fac7ade76b89dd21
    const file_path = req.body.file_path;
    try {
        const url = await main(file_path);
        res.json(url);
        
    } catch (error) {
        console.error(error);
    }
});

<<<<<<< HEAD
app.post('/put_string)', async (req, res) => {
=======
app.post('/put_string', async (req, res) => {
>>>>>>> 5fffe3fa207e9dc84246da57fac7ade76b89dd21
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