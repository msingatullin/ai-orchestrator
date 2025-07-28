from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def admin_home() -> str:
    """Minimal admin interface placeholder."""
    return "<html><body><h1>Admin Panel</h1><p>Welcome.</p></body></html>"
