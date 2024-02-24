from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, user, users

# Create the FastAPI app
app = FastAPI()
origins = ["*"]
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(users.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Define a simple route for testing
@app.get("/")
def get_app():
    return "hey dude, this is iam"
