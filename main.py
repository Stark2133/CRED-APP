from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

# -----------------MODELS-------------------
class userLogin(BaseModel):
    name: str
    password: int

class userRegister(BaseModel):
    name: str
    email: str
    age: int
    isAdmin: bool

# -------------------ROUTES-----------------
@app.get('/')
def home():
    return {'message': 'dukaan khuli hai'}

@app.post('/login')
def login(data: userLogin):
   return{
       'name': data.name,
       'password': data.password,
   }

@app.post("/signup")
def signup(data: userRegister):
    if data.isAdmin == True and data.age > 18 and '@' in data.email:
        return{
            'message': 'Registered successfully',
            'name': data.name,
            'isAdmin': data.isAdmin,
        }