from fastapi import APIRouter
from app.simulation.network import default_network

router = APIRouter()

@router.get("/")
def get_network():
    """Returns the current traffic network topology (nodes and edges)."""
    return default_network.to_dict()
