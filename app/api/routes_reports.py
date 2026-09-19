from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.post("/generate")
def generate_report():
    return {"status": "generated", "report_url": "/reports/1.pdf"}