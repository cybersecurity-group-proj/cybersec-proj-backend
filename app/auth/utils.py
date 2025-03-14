import jwt.exceptions
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.db.config import Config
import uuid
import logging


passwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_passwd(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + expiry if expiry else datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    print(f"JWT_ALGORITHM: '{Config.JWT_ALGORITHM}'")

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM

    )
    return token

def decode_token(token: str) -> dict:

    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,  
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    
    except jwt.PyJWTError as e:
        logging.error(e)