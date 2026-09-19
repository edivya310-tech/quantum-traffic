from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/comparison", tags=["Comparison"])

@router.post("/run")
def run_comparison():
    return {
        "fixed_time": {"average_waiting_time": 10.0, "maximum_queue": 5, "throughput": 100, "fuel_consumption": 5.0, "co2_emission": 12.0, "runtime": 1.0},
        "rule_based": {"average_waiting_time": 8.0, "maximum_queue": 4, "throughput": 110, "fuel_consumption": 4.5, "co2_emission": 10.8, "runtime": 1.2},
        "hybrid_quantum": {"average_waiting_time": 5.0, "maximum_queue": 2, "throughput": 130, "fuel_consumption": 3.8, "co2_emission": 9.1, "runtime": 5.5}
    }