from typing import TypedDict, Optional, List

class AgentState(TypedDict, total = False):
  question: str
  modified_question: Optional[List[str]]
  decision: dict
  answer: Optional[str]
  docs: Optional[list]
  rag_artifact: Optional[dict]
  sql_artifact: Optional[dict]
  are_docs: Optional[bool]
  rag_success: bool
  final_action: str