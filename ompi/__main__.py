from fastapi import FastAPI
from .utils.loader import load_packages
import uvicorn

app = FastAPI()
packages = load_packages()

@app.get("/")
def read_root():
    return "Hello, World!"

@app.get("/project/{name}")
def project(name: int):
    return packages[name]["html"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
