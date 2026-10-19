from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.config import get_followup_policy
from app.core.database import SessionLocal
from app.models import Followup, Lead


def is_quiet_hours() -> bool:
    policy = get_followup_policy()
    tz = ZoneInfo(policy["timezone"])
    now = datetime.now(tz).time()
    start = time.fromisoformat(policy["quiet_hours"]["start"])
    end = time.fromisoformat(policy["quiet_hours"]["end"])
    if start > end:  # raat wala window (jaise 21:00 se 09:00)
        return now >= start or now < end
    return start <= now < end


def find_due_leads(db: Session) -> list[Lead]:
    policy = get_followup_policy()
    cadence = policy["cadence_hours"]
    now = datetime.utcnow()

    leads = (
        db.query(Lead)
        .filter(Lead.status.notin_(policy["stop_statuses"]))
        .filter(Lead.telegram_id.isnot(None))
        .all()
    )

    due = []
    for lead in leads:
        attempts = (
            db.query(Followup)
            .filter(Followup.lead_id == lead.id, Followup.status == "sent")
            .count()
        )
        if attempts >= policy["max_attempts"] or attempts >= len(cadence):
            continue
        last = lead.last_contacted_at or lead.created_at
        if now >= last + timedelta(hours=cadence[attempts]):
            due.append(lead)
    return due


def process_lead(lead_id: int) -> None:
    """Placeholder: yahan baad mein LangGraph agent judega."""
    print(f"[scheduler] process_lead called for lead {lead_id}")


def run_followup_job() -> None:
    if is_quiet_hours():
        print("[scheduler] quiet hours chal rahe hain, kuch nahi bheja")
        return

    db = SessionLocal()
    try:
        due = find_due_leads(db)
        print(f"[scheduler] {len(due)} lead(s) due hain")
        for lead in due:
            process_lead(lead.id)
    finally:
        db.close()