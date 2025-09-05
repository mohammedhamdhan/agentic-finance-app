def explain_risk(topic: str) -> str:
    notes = {
        "diversification": "Diversification can reduce idiosyncratic risk but not systemic risk.",
        "drawdown": "Max drawdown measures the largest peak-to-trough decline over a period.",
    }
    return notes.get(topic.lower(), "Risk concept not found.")
