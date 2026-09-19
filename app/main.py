from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import (
    routes_health,
    routes_network,
    routes_simulation,
    routes_optimization,
    routes_emergency,
    routes_events,
    routes_metrics,
    routes_comparison,
    routes_reports,
    routes_demo
)

app = FastAPI(
    title=settings.APP_NAME,
    description="Quantum-Enhanced Adaptive Urban Traffic Optimization Platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes_health.router)
app.include_router(routes_network.router)
app.include_router(routes_simulation.router)
app.include_router(routes_optimization.router)
app.include_router(routes_emergency.router)
app.include_router(routes_events.router)
app.include_router(routes_metrics.router)
app.include_router(routes_comparison.router)
app.include_router(routes_reports.router)
app.include_router(routes_demo.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API. Visit /docs for documentation."}
