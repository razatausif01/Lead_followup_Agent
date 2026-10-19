import httpx

from app.config import get_settings


def _url(method: str) -> str:
    return f"https://api.telegram.org/bot{get_settings().TELEGRAM_TOKEN}/{method}"


def send_message(chat_id: str, text: str) -> dict:
    resp = httpx.post(
        _url("sendMessage"),
        json={"chat_id": chat_id, "text": text},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_updates(offset: int | None = None, timeout: int = 30) -> list[dict]:
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    resp = httpx.get(_url("getUpdates"), params=params, timeout=timeout + 10)
    resp.raise_for_status()
    return resp.json().get("result", [])