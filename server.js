require('dotenv').config()

const express = require('express')
const jwt = require('jsonwebtoken')
const app = express()
app.use(express.json())

app.listen(3000)


const posts = [
    {
        username: "jh",
        title: "Hello world"
    }, {
        username: "john",
        title: "Jack and jill went up a hill"
    }
]


app.get("/posts", authenticateToken, (req, res) => {
    return res.json(posts.filter(post => post.username === req.user.name))
})


app.post("/login", (req, res) => {
    //Authenticate user
    const username = req.body.username

    if (username == null) {
        return res.sendStatus(400)
    }
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

