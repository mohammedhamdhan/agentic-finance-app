from typing import TypedDict, Literal, Dict, Any, List, Optional

Route = Literal["screen","fund","backtest","risk","other"]

class AgentState(TypedDict, total=False):
    input: str
    intent: Optional[Route]
    blocked: bool
    message: str
    artifacts: Dict[str, Any]
    history: List[Dict[str, Any]]  # optional chat history
