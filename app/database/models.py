from sqlalchemy import Column, String, Integer, Float, Boolean, JSON
from app.database.database import Base

class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    
    id = Column(String, primary_key=True, index=True)
    timestamp = Column(Float, index=True)
    scenario = Column(String)
    duration = Column(Float)
    random_seed = Column(Integer)
    traffic_level = Column(String)
    solver = Column(String)
    
class MetricRecord(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    run_id = Column(String, index=True)
    timestamp = Column(Float, index=True)
    data = Column(JSON)
