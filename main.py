import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema
from app.model import UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import JwtBearer

posts = [
    {
        "id": 1,
        "title": "Penguins",
        "content": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers",
        "content": "Tigers are the larges living cat species and a members of the genus Panthera."
    },
    {
        "id": 3,
        "title": "Koalas",
        "content": "Koala is arboreal herbivorous marsupial native to Australia."
    }
]

users = []

app = FastAPI()

# get home
@app.get("/", tags=["home"])
def greet():
    return {"Hello": "World!"}

# get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}

# get single post by id
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {"error": "Post with this ID does not exist."}
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


# post a blog post [a handler for creating a post]
@app.post("/posts", dependencies=[Depends(JwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post added."
    }

# user signup (create a new user)
@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False

@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details."
        }