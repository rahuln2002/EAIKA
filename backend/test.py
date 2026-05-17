from app.core.security.jwt_handler import (
    create_access_token,
    decode_access_token,
)

data = {
    "sub": "rahul",
    "email": "rahul@example.com",
}

token = create_access_token(data)

print("TOKEN:")
print(token)

print()

decoded = decode_access_token(token)

print("DECODED:")
print(decoded)
