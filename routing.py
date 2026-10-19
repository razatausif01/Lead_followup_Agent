from typing import Literal

from app.graph.state import LeadState

MAX_REGEN = 2          # guardrail reject hone par kitni baar dobara generate karna hai
MAX_SEND_RETRY = 2     # send fail hone par kitni baar try karna hai


def route_after_policy(state: LeadState) -> Literal["retrieve_context", "__end__"]:
    """check_policy ke baad: stop_status / max_attempts / too_early ho to yahin band."""
    if state.get("should_stop"):
        return "__end__"
    return "retrieve_context"


def route_after_generate(state: LeadState) -> Literal["guardrail_check", "update_lead"]:
    """generate_message ke baad: LLM ne bola send nahi karna to seedha update_lead."""
    if state.get("llm_should_send") and state.get("draft_message"):
        return "guardrail_check"
    return "update_lead"


def route_after_guardrail(
    state: LeadState,
) -> Literal["send_message", "generate_message", "update_lead"]:
    """guardrail pass -> bhejo, fail -> limit tak regenerate, phir bhejna band."""
    if state.get("guardrail_passed"):
        return "send_message"
    if state.get("regen_count", 0) < MAX_REGEN:
        return "generate_message"
    return "update_lead"


def route_after_send(state: LeadState) -> Literal["send_message", "update_lead"]:
    """send fail hua to limit tak retry, warna update_lead."""
    if state.get("send_status") == "failed" and state.get("send_retry_count", 0) < MAX_SEND_RETRY:
        return "send_message"
    return "update_lead"