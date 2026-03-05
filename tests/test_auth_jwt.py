import jwt
from app.auth.jwt import create_access_token, decode_access_token
from app.config import settings

def test_create_and_decode_token():
    data = {"sub": "12345"}
    token = create_access_token(data)
    
    assert token is not None
    decoded = decode_access_token(token)
    assert decoded["sub"] == "12345"
    assert "exp" in decoded

def test_invalid_token():
    invalid_token = jwt.encode({"sub": "123"}, "wrong_secret", algorithm="HS256")
    decoded = decode_access_token(invalid_token)
    assert decoded is None
