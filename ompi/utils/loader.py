from pathlib import Path
import markdown
import toml

ROOT_DIR = Path(__file__).resolve().parent.parent

def merge_dicts(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            if isinstance(value, dict) and isinstance(dict1[key], dict):
                merge_dicts(dict1[key], value)  
            else:
                dict1[key] = value  
        else:
            dict1[key] = value 
    return dict1

def load_package(name):
    path = Path(ROOT_DIR, "packages", name)
    with open(Path(path, "cache.toml"), "r") as f:
        cache = toml.loads(f.read())
    
    latest = Path(path, cache["project"]["latest"])
    with open(Path(latest, "omproject.toml"), "r") as f:
        project = toml.loads(f.read())
        
    with open(Path(latest, cache["project"]["readme"]), "r") as f:
        md = f.read()

    return merge_dicts(cache, project) | { "md" : md }

def load_packages(path: Path | str = Path(ROOT_DIR, "packages")):
    packages = {extension.name: load_package(extension.name) for extension in path.iterdir()}
    return packages
        
        