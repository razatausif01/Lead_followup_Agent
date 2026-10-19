# app/graph/state.py
from typing import TypedDict, Optional, List, Dict, Any, Literal


class LeadState(TypedDict, total=False):
    # ---------- Input (graph invoke karte waqt aayega) ----------
    lead_id: int                       # LeadOut.id se match

    # ---------- load_lead node ----------
    lead: Dict[str, Any]               # name, phone, telegram_id, source, status...
    lead_status: str
    telegram_id: Optional[str]         # message yahin bhejenge
    channel: str                       # abhi hamesha "telegram"
    attempt_count: int                 # history se count hoga
    last_contacted_at: Optional[str]   # ISO string
    history: List[Dict[str, Any]]      # MessageOut format: id, lead_id, role, message, timestamp

    # ---------- check_policy node ----------
    should_stop: bool
    stop_reason: Optional[str]         # stop_status / max_attempts / too_early

    # ---------- retrieve_context node (RAG) ----------
    context_docs: List[str]

    # ---------- generate_message node (FollowupDecision) ----------
    llm_should_send: Optional[bool]    # FollowupDecision.should_send
    llm_reason: Optional[str]          # FollowupDecision.reason
    draft_message: Optional[str]       # FollowupDecision.message
    regen_count: int

    # ---------- guardrail_check node ----------
    guardrail_passed: Optional[bool]
    guardrail_reason: Optional[str]

    # ---------- send_message node ----------
    send_status: Optional[Literal["sent", "failed", "skipped"]]
    send_error: Optional[str]
    send_retry_count: int

    # ---------- update_lead node ----------
    next_followup_at: Optional[str]

    # ---------- common ----------
    errors: List[str]