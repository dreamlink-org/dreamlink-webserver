from datetime import datetime
from jwt import encode
from dreamlink.config import jwt_secret

def create_jwt(user_id, *, jwt_code):
    return encode(dict(
        user_id = user_id, 
        jwt_code = jwt_code
    ), jwt_secret, algorithm="HS256")