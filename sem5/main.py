from fastapi import FastAPI, Body, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, EmailStr
from random import choice
from faker import Faker

app = FastAPI()
fake = Faker('ru_RU')
templates = Jinja2Templates(directory="templates")


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


tasks = []

for i in range(0, 10):
    new_task = Task(
        id=i,
        title=f'title + {i}',
        description=f'description + {i}',
        status=f'status + {i}')
    tasks.append(new_task)


@app.get("/tasks/")
async def root():
    return tasks


@app.post("/tasks/")
async def create_task(task: Task):
    tasks.append(task)
    return tasks


@app.put("/tasks/{task_id}")
async def change_task(task_id: int, task: Task):
    for i, elem in enumerate(tasks):
        if elem.id == task_id:
            tasks[i] = task
            return task
    return {"message": "task not found"}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for elem in tasks:
        if elem.id == task_id:
            tasks.remove(elem)
            return {"message": "task removed"}
    return {"message": "task not found"}


# Создать API для получения списка фильмов по жанру.
# Приложение должно иметь возможность получать список фильмов по заданному жанру.
# ●	Создайте модуль приложения и настройте сервер и маршрутизацию.
# ●	Создайте класс Movie с полями id, title, description и genre.
# ●	Создайте список movies для хранения фильмов.
# ●	Создайте маршрут для получения списка фильмов по жанру (метод GET).
# ●	Реализуйте валидацию данных запроса и ответа.

class Movie(BaseModel):
    id: int
    title: str | None
    description: str
    genre: str


movies = []
genres = ["Ужас", "Триллер", "Комедия", "Исторический", "Фантастика"]
for i in range(1, 11):
    new_movie = Movie(
        id=i,
        title=f"title{i}",
        description=f"description{i}",
        genre=choice(genres)
    )
    movies.append(new_movie)


@app.get("/movies/")
async def get_movies():
    return movies


@app.get("/movies/{genre}")
async def get_movies_by_genre(genre: str):
    result = []
    for movie in movies:
        if movie.genre == genre:
            result.append(movie)
    return result if result else {"message": "No movies in that genre"}


@app.post("/movies/")
async def create_movie(movie: Movie):
    movies.append(movie)
    return movie


@app.put("/movies/")
async def update_movie(movie_id: int, movie: Movie = Body(..., embed=True)):
    for i, m in enumerate(movies):
        if m.id == movie_id:
            movies[i] = movie
            return movie
    return {"message": "movie not found"}


@app.delete("/movie/")
async def delete_movie(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            movies.remove(movie)
            return {"message": "movie removed"}
    return {"message": "movie not found"}


# Создать API для добавления нового пользователя в базу данных.
# Приложение должно иметь возможность принимать POST запросы с данными нового пользователя
# и сохранять их в базу данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Реализуйте валидацию данных запроса и ответа

class User(BaseModel):
    id: int = Field(..., example="11")
    name: str = Field(..., example="Илья")
    email: EmailStr = Field(..., example="random@email.ru")
    password: str = Field(..., example="mypassword")


users = []
for i in range(1, 11):
    new_user = User(
        id=i,
        name=fake.first_name(),
        email=fake.unique.email(),
        password=fake.password()
    )
    users.append(new_user)


@app.get('/users/')
def get_user():
    return users


@app.post("/users/")
async def create_user(user: User):
    users.append(user)
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    for i, u in enumerate(movies):
        if u.id == user_id:
            users[i] = user
            return {"user_id": user_id, "user": user}
    return {"message": "user not found"}


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": "user removed"}
    return {"message": "user not found"}


# Создать веб-страницу для отображения списка пользователей.
# Приложение должно использовать шаблонизатор Jinja для динамического формирования HTML страницы.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте HTML шаблон для отображения списка пользователей.
# Шаблон должен содержать заголовок страницы, таблицу со списком пользователей
# и кнопку для добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.
@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
