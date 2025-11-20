from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.config import SECRET_KEY, ALGORITHM
from api.models.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        if token_data.sub is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        return int(token_data.sub)
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
