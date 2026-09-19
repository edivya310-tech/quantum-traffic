import json
import asyncio
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List

from app.api.auth import get_current_user
from app.services.llm_client import generate_response
from app.simulation.simulator import simulator_engine

router = APIRouter()

class SignalTimingRecommendation(BaseModel):
    node_id: str = Field(description="The ID of the intersection/node")
    suggested_green_time: float = Field(description="Suggested green time duration in seconds")
    reasoning: str = Field(description="Brief reason for the suggestion")

class RecommendationResponse(BaseModel):
    recommendations: List[SignalTimingRecommendation]

def _get_current_state_summary() -> str:
    state_desc = f"Simulation Time: {simulator_engine.current_time:.1f}s\n"
    waiting = sum(1 for v in simulator_engine.vehicles.values() if v.status == "waiting")
    moving = len(simulator_engine.vehicles) - waiting
    state_desc += f"Active Vehicles: {len(simulator_engine.vehicles)} ({moving} moving, {waiting} waiting)\n"
    state_desc += "Signals and Queues:\n"
    for node_id, sig in simulator_engine.signals.items():
        queues = {edge: 0 for edge in sig.incoming_edges}
        for v in simulator_engine.vehicles.values():
            if v.status == "waiting" and v.current_edge_index < len(v.route) - 1:
                current_u = v.route[v.current_edge_index]
                if v.route[v.current_edge_index + 1] == node_id:
                    if current_u in queues:
                        queues[current_u] += 1
        state_desc += f" - Intersection {node_id}:\n"
        state_desc += f"   Current Green: {sig.current_green_edge} (active for {sig.time_since_last_change:.1f}s)\n"
        for edge, q in queues.items():
            state_desc += f"   Queue from {edge}: {q} vehicles\n"
    return state_desc

@router.post("/explain")
async def explain_congestion(user: dict = Depends(get_current_user)):
    state_summary = _get_current_state_summary()
    messages = [
        {"role": "system", "content": "You are an AI traffic advisory system. Explain the current congestion based on the provided state summary in plain English. Keep it concise."},
        {"role": "user", "content": f"Current State:\n{state_summary}"}
    ]
    response = await generate_response(messages=messages, stream=False)
    return {"explanation": response.choices[0].message.content}

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_timings(user: dict = Depends(get_current_user)):
    state_summary = _get_current_state_summary()
    messages = [
        {"role": "system", "content": "You are an AI traffic advisory system. Recommend signal timing changes for the intersections based on current queues."},
        {"role": "user", "content": f"Current State:\n{state_summary}"}
    ]
    response = await generate_response(messages=messages, stream=False, response_format=RecommendationResponse)
    return response.choices[0].message.parsed

class ChatMessage(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_network(chat_msg: ChatMessage, user: dict = Depends(get_current_user)):
    state_summary = _get_current_state_summary()
    messages = [
        {"role": "system", "content": "You are an AI traffic advisory system helping a traffic operator. You have access to the current state."},
        {"role": "user", "content": f"System Context:\n{state_summary}"},
        {"role": "user", "content": chat_msg.message}
    ]
    
    response = await generate_response(messages=messages, stream=True)
    
    async def sse_generator():
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(sse_generator(), media_type="text/event-stream")
