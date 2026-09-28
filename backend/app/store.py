from typing import Dict
from app.models.schemas import RepositoryResponse
import json
import os

# In-memory store for repositories mapped by repository_id
REPOSITORIES: Dict[str, RepositoryResponse] = {}

# session_id format: secure random hex string
SESSIONS: Dict[str, dict] = {}

# CSRF state store for OAuth
OAUTH_STATES: Dict[str, bool] = {}

CACHE_FILE = "repo_cache.json"

def save_cache():
    try:
        with open(CACHE_FILE, "w") as f:
            data = {k: v.model_dump() for k, v in REPOSITORIES.items()}
            json.dump(data, f)
    except Exception as e:
        print("Failed to save cache:", e)

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    REPOSITORIES[k] = RepositoryResponse.model_validate(v)
        except Exception as e:
            print("Failed to load cache:", e)

load_cache()
