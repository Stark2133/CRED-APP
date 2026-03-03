from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from models import Base
from models import User
from database import SessionLocal
from sqlalchemy.orm import session
Base.metadata.create_all(bind=engine)
app = FastAPI()



# -----------------MODELS-------------------
class userLogin(BaseModel):
    name: str
    password: int

class userRegister(BaseModel):
    name: str 
    email: str
    password: str

# -------------------ROUTES-----------------

@app.put('/users/{user_id}')
def update(user_id: int, data: userRegister):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        db.close()
        return{'message': 'No id found'}
    existing_user.name = data.name
    existing_user.email = data.email
    existing_user.password = data.password

    db.commit()
    db.refresh(existing_user)
    db.close()
    return{'message': 'Updated successfully'}

@app.get('/users')
def user_data():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    db.close()

    if user is None:
        return {"error": "User not found"}

    return user

@app.get('/')
def home():
    return {'message': 'dukaan khuli hai'}
 
@app.post('/login')
def login(data: userLogin):
   return{
       'name': data.name,
       'password': data.password,
   }

@app.post("/register")
def register(data: userRegister):
    db = SessionLocal()
    newUser = User(
        name = data.name,
        email = data.email,
        password = data.password
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    db.close()
    return{'message': 'user created susccessfully'}