# CS3219-C
CS3219 Task C

# Link to Github
https://github.com/Jh123x/CS3219-C

# Quick Start Guide
- Clone the repo using `git clone https://github.com/Jh123x/CS3219-C.git`
- Install the requirements using `npm install`
- Run `npm run devStart` to start the nodemon server (For debug)
- The server is not running at `localhost:3000`

# Endpoints
## GET `/posts`
No argument required

Will retrieve the posts posted by the user.

If the user is an admin, returns all the posts.

## GET `/admin`
No argument required.

Will return the permission level of the person if they are an admin.


## POST `/posts`
`title` required for the post.

Creates a post for the current user.


## POST `/login`
`username` and `password` required.

Logs in a returns a token for the user.


## POST `/register/`
`username` and `password` required.

Register the user.



# Things to note
- In memory DB is used as a proof of concept
