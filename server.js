require('dotenv').config()

const express = require('express')
const jwt = require('jsonwebtoken')
const app = express()

app.use(express.json())
app.listen(3000)


// Simulate the Database
const users = {
    "jh1234": {
        username: "jh",
        password: "hello world",
        permission_level: 1 // Admin
    },
    "john": {
        username: "john",
        password: "johnny",
        permission_level: 0 // Normal user
    }
}

const posts = [
    {
        username: "jh1234",
        title: "Hello world"
    }, {
        username: "john",
        title: "Jack and jill went up a hill"
    }
]


app.get("/posts", authenticateToken, (req, res) => {
    var username = req.user.name
    const user = users[username]

    if (user == null) {
        return res.sendStatus(401)
    }

    if (user.permission_level == 1) {
        return res.json(posts)
    }
    return res.json(posts.filter(post => post.username === username))
})


app.post("/register", (req, res) => {
    const username = req.body.username
    const password = req.body.password

    if (username == null || password == null || users[username] != null) {
        return res.sendStatus(400).send("User is already found or incorrect fields")
    }
    users[username] = {
        username: username,
        password: password,
        permission_level: 0
    }
    return res.sendStatus(201)
})

app.post("/login", (req, res) => {
    //Authenticate user
    const username = req.body.username
    const password = req.body.password

    if (username == null || password == null) {
        return res.sendStatus(400)
    }

    if(users[username] == null){
        return res.sendStatus(404)
    }

    if(users[username].password != password){
        return res.sendStatus(401)
    }

    // Set up JWT
    const user = { name: username }
    const accessToken = generateAccessToken(user)
    return res.json({ accesstoken: accessToken })
})

function generateAccessToken(user) {
    return jwt.sign(user, process.env.ACCESS_TOKEN_SECRET)
}

function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization']
    const token = authHeader && authHeader.split(' ')[1]

    //Check if the token is correct
    if (token == null) {
        return res.sendStatus(401)
    }

    // JWT verify
    jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, user) => {
        if (err) {
            return res.sendStatus(403)
        }
        req.user = user
        console.log(user)
        next()
    })
}