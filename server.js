const express = require('express')
const jwt = require('jsonwebtoken')
const app = express()

app.listen(3000)
app.use(express.json())

const posts = [
    {
        username: "jh",
        title: "Hello world"
    }, {
        username: "john",
        title: "Jack and jill went up a hill"
    }
]


app.get("/posts", (req, res) => {
    return res.json(posts)
})


app.post("/login", (req, res) => {
    //Authenticate user
    const username = req.body.username
    const user = {name: username}
    
    const accessToken = jwt.sign(user, process.env.ACCESS_TOKEN_SECRET)
    return res.json({accesstoken : accessToken})
})


