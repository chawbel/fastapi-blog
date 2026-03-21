from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jinja2 import exceptions
from starlette.exceptions import HTTPException as StarletteHTTPExcpetion
from starlette.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_CONTENT
from starlette.templating import _TemplateResponse

from schemas import PostCreate, PostResponse


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), "static")

posts: list[dict] = [
    {
        "id": 1,
        "title": "FastApi tutorial",
        "author": "zobr",
        "content": "zpbran zabir",
        "date_posted": "April 20, 2013",
    },
    {
        "id": 2,
        "title": "Python tutorial",
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


@app.get("/posts/{id}", include_in_schema=False)
def post_page(request: Request, id: int):
    for post in posts:
        if post.get("id") == id:
            return templates.TemplateResponse(
                request,
                context={"post": post, "title": post["title"]},
                name="post.html",
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts


@app.get("/api/posts/{id}", response_model=PostResponse)
def get_post(id: int):
    for post in posts:
        if post.get("id") == id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post("/api/posts",
          status_code=HTTP_201_CREATED,
          response_model=PostCreate)
def create_post(post: PostCreate):
    new_id: int = max(p["id"] for p in posts) + 1 if posts else 1
    new_post: dict = {
            "id": new_id,
            "author": post.author,
            "title": post.title,
            "content": post.content,
            "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post


@app.exception_handler(StarletteHTTPExcpetion)
def general_exception_handler(request: Request, exception: StarletteHTTPExcpetion):
    message = (
        exception.detail
        if exception.detail
        else "Invalid input. Please check your request and try again"
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code, content={"detail": message}
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        context={
            "message": message,
            "title": exception.status_code,
            "status_code": exception.status_code,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        context={
            "message": "Invalid input please check your request and try again.",
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
