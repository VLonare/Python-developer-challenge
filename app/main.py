from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, todos
from app.db import DATABASE

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(todos.router, prefix="/todos", tags=["To-Do Items"])


from fastapi import FastAPI, HTTPException

app = FastAPI()

class ItemNotFoundError(HTTPException):
    def __init__(self, item_id: int):
        detail = f"Item with ID {item_id} not found"
        super().__init__(status_code=404, detail=detail)


@app.exception_handler(ItemNotFoundError)
async def item_not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


