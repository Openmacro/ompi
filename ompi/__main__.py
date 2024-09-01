from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .utils.loader import load_packages, ROOT_DIR
from pathlib import Path
import uvicorn

app = FastAPI()
packages = load_packages()
projects = Jinja2Templates(directory=Path(ROOT_DIR, "client", "templates", "project"))
app.mount("/static", StaticFiles(directory=Path(ROOT_DIR, "client", "static")), name="static")

@app.get("/")
def read_root():
    return "Hello, World!"

@app.get("/project/{name}", response_class=HTMLResponse)
def project(request: Request, name: str):
    project_data = {
        "name": name,
        "version": packages[name]["project"]["latest"],
        "description": packages[name]["project"]["description"],
        "license": packages[name]["project"]["license"],
        "src": packages[name]["setup"]["source"],
        "maintainers": packages[name]["project"]["authors"],
        "readme": packages[name]["md"]
    }
    return projects.TemplateResponse("index.html", {"request": request, **project_data})

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
