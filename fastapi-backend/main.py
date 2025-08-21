import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:5173", "127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/api", summary="Main root", tags=["Main endpoints"])
async def root():
    """
    root \n
    returns json {"message":"Hello, World!"}
    """
    return {
        "message": "Hello, World!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)