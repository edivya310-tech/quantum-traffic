from fastapi import APIRouter
from app.schemas.network import NetworkSchema, IntersectionSchema, RoadSchema
from typing import List

router = APIRouter(prefix="/api/v1/network", tags=["Network"])

@router.get("/", response_model=NetworkSchema)
def get_network():
    # Placeholder for default 4-intersection network
    return NetworkSchema(id="default", name="Default 4-Intersection Network")

@router.get("/intersections", response_model=List[IntersectionSchema])
def get_intersections():
    # Placeholder
    return []

@router.get("/roads", response_model=List[RoadSchema])
def get_roads():
    # Placeholder
    return []
