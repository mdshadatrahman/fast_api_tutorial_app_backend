from fastapi import FastAPI
import models
from database import engine
import routers
# from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.post.router)
app.include_router(routers.user.router)
app.include_router(routers.auth.router)
app.include_router(routers.vote.router)


@app.get("/")
def root():
    return {"Hello": "WELCOME TO THE API WORLD"}
