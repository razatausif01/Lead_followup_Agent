from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------- API input / output ----------
class LeadCreate(BaseModel):
    name: str
    phone: str | None = None
    telegram_id: str | None = None
    source: str | None = None


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str | None
    telegram_id: str | None
    source: str | None
    status: str
    created_at: datetime
    last_contacted_at: datetime | None


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    role: str
    message: str
    timestamp: datetime


# ---------- LLM structured outputs ----------
class FollowupDecision(BaseModel):
    should_send: bool
    message: str
    reason: str


class LeadIntent(BaseModel):
    intent: str  # interested / not_interested / question / opt_out / other
    summary: str