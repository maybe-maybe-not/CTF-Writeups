import random
import string
import re

import databases
import sqlalchemy
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

DATABASE_URL = "sqlite:///./users.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
)

flags = sqlalchemy.Table(
    "flags",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("flag", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def generate_password():
    character_set = string.ascii_letters + string.digits
    return "".join(random.choice(character_set) for i in range(64))


def is_sqli(check):  # NotHandSanitizer™ SQL Injection Sanitizer
    m = re.match(
        r".*([\[\]\{\}:\\|;?!~`@#$%^&*()_+=-]|[ ]|[']|[\"]|[<]|[>]).*",
        check,
        re.MULTILINE,
    )
    if m is not None:
        return True
    return False


@app.on_event("startup")
async def startup():
    await database.connect()

    for user in ['adam', 'admin', 'bob', 'gina', 'charlie']:
        create_user = users.insert().values(
            username=user, password=generate_password()
        )
        await database.execute(create_user)

    with open('flag.txt', 'r') as f:
        flag = f.read()

    create_flag = flags.insert().values(
        username='admin', flag=flag
    )

    await database.execute(create_flag)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login/", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        if is_sqli(username) or is_sqli(password):
            return "Login failed!"
        query = f"SELECT username FROM users WHERE username='{username}' AND password='{password}'"
        logged_in_user = await database.fetch_one(query=query)
        if not logged_in_user:
            return "Login failed!"
        if logged_in_user['username'] != 'admin':
            return "Not authorized!"
        return "Welcome to Apocalypse"
    except:
        return "Login failed!"
