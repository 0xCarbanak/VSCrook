const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
app.get('/', (req, res) => res.json({ status: 'ok' }));
app.get('/api/users', (req, res) => res.json([{ id: 1, name: 'John' }]));
app.listen(PORT);
module.exports = app;
