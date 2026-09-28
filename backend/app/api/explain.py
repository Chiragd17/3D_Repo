from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ExplainRequest, ExplainResponse
from app.store import REPOSITORIES, SESSIONS
import os
import json
import httpx
from groq import AsyncGroq
from app.github.client import get_headers, GITHUB_API_URL

router = APIRouter()

@router.post("/explain", response_model=ExplainResponse)
async def explain_file(body: ExplainRequest, request: Request):
    repo_data = REPOSITORIES.get(body.repository_id)
    if not repo_data:
        raise HTTPException(status_code=404, detail="Repository not found")
        
    file_intel = next((f for f in repo_data.files if f.id == body.file_id), None)
    if not file_intel:
        raise HTTPException(status_code=404, detail="File not found")

    owner = repo_data.repository.owner
    repo = repo_data.repository.name
    path = file_intel.path

    # Get token for private repos
    session_id = request.cookies.get("session_id")
    token = SESSIONS.get(session_id, {}).get("github_access_token") if session_id else None

    # Fetch file content from GitHub directly
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_headers(token))
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch file content from GitHub")
            
        data = response.json()
        if data.get("encoding") == "base64":
            import base64
            try:
                content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")
            except Exception:
                content = ""
        else:
            content = ""
            
    if not content:
         return ExplainResponse(
            file_id=body.file_id,
            summary="Could not fetch file content.",
            keyComponents=[],
            potentialIssues=[]
        )
        
    # Use Groq to explain
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is missing")
    
    groq_client = AsyncGroq(api_key=groq_api_key)
    prompt = f"Explain this code file '{path}':\n\n{content[:5000]}\n\nRespond in strictly valid JSON with three keys: 'summary' (string), 'keyComponents' (list of strings), 'potentialIssues' (list of strings). No markdown formatting, just JSON."
    
    try:
        chat_completion = await groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            response_format={"type": "json_object"}
        )
        
        result = json.loads(chat_completion.choices[0].message.content)
        return ExplainResponse(
            file_id=body.file_id,
            summary=result.get("summary", "No summary available."),
            keyComponents=result.get("keyComponents", []),
            potentialIssues=result.get("potentialIssues", [])
        )
    except Exception as e:
        return ExplainResponse(
            file_id=body.file_id,
            summary=f"Failed to generate AI explanation: {str(e)}",
            keyComponents=[],
            potentialIssues=[]
        )
