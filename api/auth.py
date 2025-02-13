from fastapi import Header, HTTPException
from config import STATIC_TOKEN

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    token = authorization.split(" ")[1]
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
