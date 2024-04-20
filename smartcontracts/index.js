const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;
app.use(express.json());
const { push, new_room, get_commits }= require('./scripts/interact.js');

const API = axios.create({
    baseURL: 'http://localhost:8000',
});

app.post('/new_room', (req, res) => {
    const room_id = req.body.room_id;
    const members=req.body.members;
    new_room(room_id, members);
});
app.post('/push', (req, res) => {
    const commit = req.body.commit;
    const room_id=req.body.room_id;
    push(commit, room_id);
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

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});


