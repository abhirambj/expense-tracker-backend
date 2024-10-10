from fastapi import APIRouter, HTTPException
from models.user import CreateUser, UserLogin
from passlib.context import CryptContext
from uuid import uuid4, UUID

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory storage of users
users = []


def hash_password(password):
    return pwd_context.hash(password)


@router.get("/users/")
def get_users():
    return {"users": users}


@router.post("/users/")
def create_user(user: CreateUser):
    # Check if passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if user with this email or username already exists
    for existing_user in users:
        if existing_user["email"].lower() == user.email.lower():
            raise HTTPException(status_code=400, detail="User with this email already exists")
        if existing_user["username"].lower() == user.username.lower():
            raise HTTPException(status_code=400, detail="User with this username already exists")

    # Generate a UUID for the new user
    user_id = str(uuid4())

    # If everything is fine, hash the password and save the user
    hashed_password = hash_password(user.password)

    new_user = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }

    users.append(new_user)
    return {"message": "User created successfully",
            "user": {"user_id": user_id, "username": user.username, "email": user.email}}


@router.get("/users/{user_id}")
def get_user(user_id: UUID):
    # Find the user by UUID
    for user in users:
        if user["id"] == str(user_id):
            return {"user": {"user_id": user["id"], "username": user["username"], "email": user["email"]}}

    # If user is not found, raise a 404 error
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/users/login/")
def login_user(user: UserLogin):
    # Find the user by username
    for existing_user in users:
        if existing_user["username"].lower() == user.username.lower():
            # Check if the password is correct
            if pwd_context.verify(user.password, existing_user["password"]):
                return {
                    "message": "Login successful",
                    "user": {
                        "user_id": existing_user["id"],
                        "username": existing_user["username"],
                        "email": existing_user["email"],
                    },
                }
            break  # Exit the loop if username matched but password was incorrect
    raise HTTPException(status_code=400, detail="Invalid credentials")


