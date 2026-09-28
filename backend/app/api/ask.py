from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse, Target

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    return AskResponse(
        answer="Authentication is primarily handled by the authentication service.",
        targets=[
            Target(
                file_id="src-auth-auth-service",
                path="src/auth/auth_service.py",
                reason="Contains authentication and token validation logic."
            )
        ]
    )
