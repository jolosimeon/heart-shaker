const express = require('express');
const { Client } = require('pg');
const port = process.env.PORT || 3003;

var app = express();

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: true,
});

client.connect();

app.get('/', (req, res) => {
 res.send(JSON.stringify({ Hello: 'heart-shaker'}));
});

app.get('/user', (req, res) => {

});

app.get('/user/:id', (req, res) => {

});

app.listen(port, function () {
 console.log('App listening on port '+ port);
});