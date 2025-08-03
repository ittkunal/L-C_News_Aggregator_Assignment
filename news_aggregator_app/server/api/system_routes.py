from fastapi import APIRouter

router = APIRouter()

@router.get("/system/status")
def system_status():
    """
    Returns basic system health and external API source statuses.
    """
    # TODO: Implement actual status checks here, this is stub data
    return {
        "server": "running",
        "uptime": "72 hours",
        "external_sources": [
            {"name": "NewsAPI", "status": "active", "last_accessed": "2025-03-21T10:23:00Z"},
            {"name": "The News API", "status": "active", "last_accessed": "2025-03-21T10:21:00Z"}
        ]
    }
