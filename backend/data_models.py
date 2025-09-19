# backend/data_models.py
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class AutonomousDrivingEvent(BaseModel):
    start_location: str
    end_location: str
    passengers: int
    timestamp: Optional[str] = None
    road: Optional[str] = None
    event_type: Optional[str] = None
    severity: Optional[int] = None
    vehicles: Optional[int] = None
    lanes_blocked: Optional[int] = None
    agent_latency_ms: Optional[float] = None
    cache_hit: Optional[int] = None
    clearance_time_s: Optional[float] = None
    reroute_delay_s: Optional[float] = None
    is_congested: Optional[int] = None



class TrafficData(BaseModel):
    location: str = Field(min_length=1)
    traffic_volume: int = Field(ge=0, le=1000)

    @field_validator("location")
    @classmethod
    def non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("location cannot be empty or all spaces")
        return v.strip()


class WeatherAlert(BaseModel):
    alert_type: str = Field(min_length=1)
    area: str = Field(min_length=1)
    location: Optional[str] = None
    severity: Optional[int] = None


class ParkingData(BaseModel):
    location: str = Field(min_length=1)
    available_spots: int = Field(ge=0, le=10000)


class SafetyData(BaseModel):
    location: str = Field(min_length=1)
    safety_status: Literal["ok", "warning", "incident"]
    require_human_intervention: Optional[bool] = None


class DispatchEventRequest(BaseModel):
    event: str
    location: str
    data: Optional[dict] = None


class GenerateReportRequest(BaseModel):
    events: list


class ReportRequest(BaseModel):
    location: Optional[str] = None
    event: Optional[str] = None
    safetyStatus: Optional[str] = None
    fireResponse: Optional[dict] = None
    weatherAlert: Optional[str] = None


class FireResponse(BaseModel):
    level: Literal["low", "medium", "high", "unknown"]
    units: int


class TrafficIncident(BaseModel):
    description: str
    location: str
    severity: int