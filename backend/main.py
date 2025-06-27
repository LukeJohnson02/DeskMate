from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from Database.database import Base, engine
from Routers import user_router, ticket_router, category_router, auth_router

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(ticket_router.router)
app.include_router(category_router.router)


@app.get("/")
def root():
    return {"message": "Backend is live"}


if __name__ == "__main__":
    run(
        "main:app",
        use_colors=True,
    )
