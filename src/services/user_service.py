
from fastapi import Depends, HTTPException, Request
from database_connection import get_db
from src.models.user_model import User
from src.schemas.user_schema import LoginUser, CreateUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette import status
from starlette.responses import JSONResponse
from jose import JWTError, jwt
from datetime import timedelta
import datetime as dt
import env

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
    ) -> User:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header"
            )

        token = auth_header[len("Bearer "):]

        try:
            payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

class UserService:

    async def login(
        self,
        db: Session,
        schema: LoginUser
    ):
        user = db.query(User).filter(User.email == schema.email).first()

        if not user or not self.check_password(schema.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="E-mail or password is incorrect"
            )

        token_data = {"sub": user.email}
        token = self.create_access_token(token_data)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }

    async def create_user(
        self, 
        db: Session,
        schema: CreateUser
    ):
        
        user_exist = db.query(User).filter(User.email == schema.email).first()

        if user_exist:
             raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This e-mail already exists"
            )

        hashed_password = self.hash_password(schema.hashed_password)

        user = User(
            email=schema.email, 
            hashed_password=hashed_password, 
            role=schema.role, 
            name=schema.name
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return JSONResponse(
            content={
                "id": user.id, 
                "email": user.email
            }, 
            status_code=status.HTTP_201_CREATED
        )

    @staticmethod
    def hash_password(password):
        """
        Hash the given password using a suitable hashing algorithm.

        :param password: The password to be hashed
        :type password: str
        :return: The hashed password
        :rtype: str
        """
        return pwd_context.hash(password)

    @staticmethod
    def check_password(password, hashed_password):
        """
        Verify if the given password matches the hashed password.

        :param password: The plain text password to verify
        :type password: str
        :param hashed_password: The hashed password to compare against
        :type hashed_password: str
        :return: True if the password matches the hashed password, False otherwise
        :rtype: bool
        """

        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def create_access_token(data: dict):
        """
        Create a JWT access token with the provided data.

        The token includes an expiration time, which is set to a certain number
        of minutes from the current UTC time, specified by ACCESS_TOKEN_EXPIRE_MINUTES.

        :param data: The data to be included in the token payload.
        :type data: dict
        :return: The encoded JWT access token.
        :rtype: str
        """
        to_encode = data.copy()
        expire = dt.datetime.now(dt.timezone.utc) + timedelta(minutes=int(env.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)
        return encoded_jwt