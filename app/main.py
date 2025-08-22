from fastapi import FastAPI
from app.routers import auth, user, ticket, passenger  # Import client if implemented

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router)
app.include_router(ticket.router)
app.include_router(passenger.router)
# app.include_router(client.router)