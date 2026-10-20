import os
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Header, Depends, BackgroundTasks
from pydantic import BaseModel

# Router setup
router = APIRouter(prefix="/api/leads", tags=["Leads & Webhooks"])

# Secret Token for Cron authentication (Environment variable se lega)
CRON_SECRET_TOKEN = os.getenv("CRON_SECRET_TOKEN", "my_cron_secret_123")

# --- Request Schemas ---
class LeadCreateSchema(BaseModel):
    name: str
    phone_or_telegram_id: str
    source: str = "web_form"
    metadata: Optional[Dict[str, Any]] = None

class WebhookPayloadSchema(BaseModel):
    event_type: str  # e.g., "telegram_message", "new_lead"
    lead_id: Optional[str] = None
    message: Optional[str] = None
    user_data: Dict[str, Any] = {}

# --- Security Dependency for Cron Trigger ---
def verify_cron_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token format")
    token = authorization.split(" ")[1]
    if token != CRON_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized Cron execution request")


# -------------------------------------------------------------
# 1. API ENDPOINT: Manual / Frontend Lead Creation
# -------------------------------------------------------------
@router.post("/create", status_code=201)
async def create_lead(lead_data: LeadCreateSchema):
    """
    New Lead ko register karne ke liye API Endpoint.
    """
    return {
        "status": "success",
        "message": f"Lead '{lead_data.name}' successfully registered",
        "data": lead_data.model_dump()
    }


# -------------------------------------------------------------
# 2. WEBHOOK ENDPOINT: Real-time Inbound Messages / Events
# -------------------------------------------------------------
@router.post("/webhook")
async def handle_inbound_webhook(payload: WebhookPayloadSchema, background_tasks: BackgroundTasks):
    """
    Real-time webhook endpoint (Telegram ya CRM se incoming messages receive karne ke liye).
    """
    # Background task mein graph workflow trigger kar sakte hain
    return {
        "status": "received",
        "event_type": payload.event_type,
        "message": "Webhook payload received and queued for processing"
    }


# -------------------------------------------------------------
# 3. SCHEDULED CRON TRIGGER ENDPOINT: (GitHub Actions Mon-Fri)
# -------------------------------------------------------------
@router.post("/process-scheduled", dependencies=[Depends(verify_cron_token)])
async def process_scheduled_leads(background_tasks: BackgroundTasks):
    """
    GitHub Actions Mon-Fri Cron schedule se call hone wala endpoint.
    """
    return {
        "status": "success",
        "message": "Mon-Fri scheduled batch automation started"
    }


# -------------------------------------------------------------
# 4. API ENDPOINT: Fetch Lead Details / Status
# -------------------------------------------------------------
@router.get("/{lead_id}")
async def get_lead_status(lead_id: str):
    """
    Lead ka status check karne ke liye endpoint.
    """
    return {
        "lead_id": lead_id,
        "status": "active"
    }
