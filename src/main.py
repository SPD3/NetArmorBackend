from typing import List
import strawberry

from fastapi import Depends, FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
from strawberry.types import Info
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/AccountExists")
def account_exists():
    print("YAYAYAYAYAYAYAYAYAYAYAYAYYA")
    return True



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/CreateAccount/")
def create_account(account : schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=account.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=account)
    return True

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


async def get_context(
    db=Depends(get_db),
):
    return {
        "db": db,
    }

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
    
    @strawberry.field
    def user(self, id : int, info: Info) -> str:
        db = info.context['db']
        db_user = crud.get_user(db, user_id=id)
        if db_user is None:
            return "No user with id: " + str(id)
        return "user email is: " + str(db_user.email)

schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")