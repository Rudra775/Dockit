from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from Dockit Backend!"}

@app.get("/test")
async def test():
    return {"status": "ok", "environment": os.environ.get("ENV", "development")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)