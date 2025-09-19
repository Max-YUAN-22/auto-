# backend/api_routes.py
import asyncio
import json
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks
from .data_models import (
    AutonomousDrivingEvent,
    TrafficData,
    WeatherAlert,
    ParkingData,
    SafetyData,
    DispatchEventRequest,
    GenerateReportRequest,
    TrafficIncident,
)
from .dsl_workflows import (
    fire_alert_workflow_task,
    master_workflow_chain_task,
    traffic_incident_workflow_task,
    smart_city_simulation_workflow,
    generate_report_workflow,
)
from core.llm import generate_report_with_deepseek
from dsl.dsl import DSL

from agents.traffic_monitor_agent import TrafficMonitorAgent
from agents.weather_agent import WeatherAgent
from agents.parking_agent import ParkingAgent
from agents.safety_agent import SafetyAgent
from agents.traffic_incident_agent import TrafficIncidentAgent
from .dependencies import (
    get_dsl_instance,
    get_traffic_monitor_agent,
    get_weather_agent,
    get_parking_agent,
    get_safety_agent,
    get_traffic_incident_agent,
)
from .socket_app import sio

router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}


@router.post("/events/autonomous_driving")
async def autonomous_driving(evt: AutonomousDrivingEvent, dsl: DSL = Depends(get_dsl_instance)):
    payload = evt.dict()
    print(f"Processing autonomous driving event: {payload}")
    asyncio.create_task(smart_city_simulation_workflow(dsl, "autonomous_driving_task", payload))
    return {"status": "received"}


@router.post("/events/traffic_monitor")
async def traffic_monitor(
    data: TrafficData, traffic_monitor_agent: TrafficMonitorAgent = Depends(get_traffic_monitor_agent)
):
    traffic_monitor_agent.monitor_traffic(data.dict())
    message = {
        "type": "traffic_monitor",
        "payload": data.dict(),
        "title": "Traffic Monitor",
    }
    print(f"Broadcasting event: {message}")
    await sio.emit('broadcast', message, room='default_room')
    return {"status": "success"}


@router.post("/events/weather_alert")
async def weather_alert(alert: WeatherAlert, weather_agent: WeatherAgent = Depends(get_weather_agent), dsl: DSL = Depends(get_dsl_instance)):
    # 处理前端发送的数据格式
    alert_data = alert.dict()
    if 'location' in alert_data and 'area' not in alert_data:
        alert_data['area'] = alert_data['location']
    
    weather_agent.trigger_weather_alert(alert_data)
    print(f"Processing weather alert event: {alert_data}")
    asyncio.create_task(smart_city_simulation_workflow(dsl, "weather_alert_task", alert_data))
    return {"status": "alert triggered"}


@router.post("/events/parking_update")
async def parking_update(data: ParkingData, parking_agent: ParkingAgent = Depends(get_parking_agent), dsl: DSL = Depends(get_dsl_instance)):
    parking_agent.update_parking_status(data.dict())
    print(f"Processing parking update event: {data.dict()}")
    asyncio.create_task(smart_city_simulation_workflow(dsl, "parking_update_task", data.dict()))
    return {"status": "updated"}


@router.post("/events/safety_inspection")
async def safety_inspection(data: SafetyData, safety_agent: SafetyAgent = Depends(get_safety_agent), dsl: DSL = Depends(get_dsl_instance)):
    # 处理前端发送的数据格式
    safety_data = data.dict()
    if 'require_human_intervention' in safety_data and 'safety_status' not in safety_data:
        safety_data['safety_status'] = 'warning' if safety_data['require_human_intervention'] else 'ok'
    
    safety_agent.monitor_safety(safety_data)
    print(f"Processing safety inspection event: {safety_data}")
    asyncio.create_task(smart_city_simulation_workflow(dsl, "safety_inspection_task", safety_data))
    return {"status": "monitoring"}



@router.post("/simulate/{event_type}")
async def start_simulation(event_type: str, dsl: DSL = Depends(get_dsl_instance)):
    """Start a smart city simulation chain based on the initial event type."""
    event_data = {"initial_event": event_type}
    asyncio.create_task(smart_city_simulation_workflow(dsl, event_type, event_data))
    return {"status": f"simulation started with {event_type}"}
async def dispatch_event(req: DispatchEventRequest, dsl: DSL = Depends(get_dsl_instance)):
    if req.event == "fire_alert":
        event_data = {"location": req.location, "details": "Dispatch event"}
        asyncio.create_task(fire_alert_workflow_task(dsl, event_data))
        return {"status": "fire_alert workflow started"}
    return {"status": "event received, but no handler defined", "event": req.event}


async def generate_and_broadcast_report(events_json: str):
    """Generates a report and broadcasts it via WebSocket."""
    report_text = await generate_report_with_deepseek(events_json)
    message = {
        "type": "analysis_report",
        "title": "City Analysis Report",
        "payload": {"report": report_text},
        "timestamp": datetime.now().isoformat()
    }
    await sio.emit('broadcast', message, room='default_room')


@router.post("/generate-report")
async def generate_report(request: GenerateReportRequest, dsl: DSL = Depends(get_dsl_instance)):
    """
    Generate a report based on the last five events.
    """
    asyncio.create_task(generate_report_workflow(dsl, request.events))
    return {"status": "report generation started"}


@router.post("/events/traffic_incident")
async def traffic_incident(
    incident: TrafficIncident, traffic_incident_agent: TrafficIncidentAgent = Depends(get_traffic_incident_agent), dsl: DSL = Depends(get_dsl_instance)
):
    traffic_incident_agent.process(incident.dict())
    message = {
        "type": "traffic_incident",
        "payload": incident.dict(),
        "title": "Traffic Incident",
    }
    print(f"Broadcasting event: {message}")
    await sio.emit('broadcast', message, room='default_room')
    asyncio.create_task(traffic_incident_workflow_task(dsl, incident.dict()))
    return {"status": "incident reported"}