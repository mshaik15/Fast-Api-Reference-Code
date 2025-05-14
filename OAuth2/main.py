from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
# Simple API
# @app.get("/test/")  
# async def test():
    # return {'Hello' : 'World'}

# Path'd  Perameter
# @app.get("/test/{item_id}/")
# async def test(item_id: str):  # <-- item_id is a string
    # return{"hello": item_id}

# Queary Perameter
# @app.get("/test/{item_id}/")
# async def test(item_id: str, query: int = 1):
    # return {"hello": item_id}