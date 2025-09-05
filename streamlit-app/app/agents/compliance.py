

ADVICE_TRIGGERS = ["should I buy", "buy now", "allocate", "how much should I invest"]

def check(msg: str) -> dict:
    lower = (msg or "").lower()
    if any(t in lower for t in ADVICE_TRIGGERS):
        return {"blocked": True, "message": "I can’t provide personal investment advice. I can help you screen assets, summarize fund documents with citations, run simple backtests, and explain risks."}
    return {"blocked": False}
