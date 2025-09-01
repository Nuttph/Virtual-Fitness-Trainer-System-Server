const express = require('express');
const app = express();
const dotenv = require('dotenv');
dotenv.config();
const port = process.env.PORT || 5000;
const cors = require('cors');

app.use(cors());

app.get('/', (req, res) => {
    res.send({ message: 'Hello World!' });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});