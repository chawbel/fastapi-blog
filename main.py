from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), "static")

posts: list[dict] = [
    {
        "id": 1,
        "author": "zobr",
        "content": "zpbran zabir",
        "date_posted": "April 20, 2013",
    },
    {
        "id": 2,
        "author": "zobran",
        "content": "zobr narr",
        "date_posted": "June 12, 2012",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, context={"posts": posts, "title": "Title"}, name="home.html"
    )


@app.get("/api/posts")
def get_posts():
    return posts
