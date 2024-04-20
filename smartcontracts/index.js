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
app.post('/push', (req, res) => {
    const commit = req.body.commit;
    const room_id=req.body.room_id;
    push(commit, room_id);
    res.send('Success!');
});
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
    const room_id = req.body.file_path;
    try {
        const url = await main(file_path);
        API.post('/api/get_file_url', { url: url })
            .then(response => {
                res.send('Success!');
            })
        res.send('Success!');
    } catch (error) {
        console.error(error);
    }
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});