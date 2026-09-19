from fastapi import APIRouter
from app.core.config import settings
import sys

router = APIRouter(prefix="/api/v1", tags=["Health"])

@router.get("/health")
def get_health():
    quantum_available = False
    try:
        import qiskit
        quantum_available = True
    except ImportError:
        pass
        
    return {
        "status": "healthy",
        "quantum_available": quantum_available and settings.ENABLE_QUANTUM,
        "sumo_available": False,  # Optional, maybe check if sumolib is installed
        "version": "1.0.0",
        "python_version": sys.version
    }
