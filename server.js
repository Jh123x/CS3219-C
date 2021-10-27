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

// Function based on permissions
const getPosts = {
    0: (res, posts, username) => res.json(posts.filter(post=>post.username == username)),
    1: (res, posts, _) => res.json(posts),
}

const admin = {
    1: (res) => res.json({'permission_level': 'admin'}),
}



app.get("/posts", authenticateToken, (req, res) => {
    const username = req.user.name
    const user = users[username]
    const permission = user.permission_level
    if (user == null) {
        return res.sendStatus(404)
    }
    if(permission in getPosts){
        return getPosts[permission](res, posts, username)
    }
    return res.sendStatus(403)
})

app.post("/posts", authenticateToken, (req, res) => {
    const username = req.user.name
    const user = users[username]
    if (user == null) {
        return res.sendStatus(404)
    }

    const title = req.body.title
    posts.push({
        username: username,
        title: title
    })
    return res.sendStatus(201)
})

app.get("/admin", authenticateToken, (req, res) => {
    const username = req.user.name
    const user = users[username]
    const permission = user.permission_level
    if (user == null) {
        return res.sendStatus(404)
    }

    if(permission in admin){
        return admin[permission](res)
    }
    return res.sendStatus(403)
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

    if (users[username] == null) {
        return res.sendStatus(404)
    }

    if (users[username].password != password) {
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
            return res.sendStatus(401)
        }
        req.user = user
        next()
    })
}