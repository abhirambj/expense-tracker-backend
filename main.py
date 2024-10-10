from fastapi import FastAPI
from routes.expenses import router as expenses_router
from routes.user import router as user_router

app = FastAPI()

app.include_router(expenses_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Personal Finance App!"}