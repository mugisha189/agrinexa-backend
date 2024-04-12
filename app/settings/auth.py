from decouple import config
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = config("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
REFRESH_SECRET_KEY = config("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7
