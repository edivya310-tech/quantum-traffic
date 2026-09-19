from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/metrics", tags=["Metrics"])

@router.get("/current")
def get_current_metrics():
    return {}

@router.get("/history")
def get_metrics_history():
    return []