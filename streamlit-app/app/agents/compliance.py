TRIGGERS = ["should i buy","buy now","sell now","allocate","how much should i invest"]

def compliance_check(text: str):
    t = (text or "").lower()
    if any(k in t for k in TRIGGERS):
        return True, ("I can’t provide personal investment advice. "
                      "Try: screeners, an ETF summary, a simple backtest, or a risk explainer.")
    return False, ""
