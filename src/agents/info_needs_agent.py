from src.agents.base_agent import BaseAgent
from typing import List, Dict, Any


class InfoNeedsAgent(BaseAgent):
    """
    Determines what specific information is required to satisfy a clarified goal.

    Sits between UserIntentAgent and OrchestratorAgent. Takes a clarified goal
    and success conditions, then outputs concrete information requirements:
    sub-queries to answer, knowledge domains to cover, and known gaps.
    """

    def __init__(self, name: str, model_name: str):
        super().__init__(name, model_name)
        self.info_requirements: List[Dict[str, Any]] = []
        self.knowledge_gaps: List[str] = []

    def act(self, clarified_goal: str, success_conditions: List[str] = None) -> str:
        """
        Analyzes the clarified goal and returns structured information requirements.

        Returns a formatted string summary; structured data available via
        self.info_requirements and self.knowledge_gaps after this call.
        """
        print(f"{self.name} (InfoNeeds) analyzing requirements for: {clarified_goal}")

        self.info_requirements = self._derive_requirements(clarified_goal, success_conditions or [])
        self.knowledge_gaps = self._identify_gaps(clarified_goal)

        summary_lines = [f"Information Requirements for: {clarified_goal}"]
        for req in self.info_requirements:
            summary_lines.append(f"  [{req['priority'].upper()}] {req['query']} — source: {req['source_type']}")
        if self.knowledge_gaps:
            summary_lines.append(f"Known gaps: {', '.join(self.knowledge_gaps)}")

        return "\n".join(summary_lines)

    def plan(self, task: str) -> List[str]:
        return [
            "Parse clarified goal into information domains",
            "Generate sub-queries for each domain",
            "Identify preferred source types per query",
            "Flag knowledge gaps and ambiguities",
            "Prioritize requirements by importance",
        ]

    def get_search_queries(self) -> List[str]:
        """Returns ordered list of search queries derived from requirements."""
        return [r["query"] for r in sorted(self.info_requirements, key=lambda x: x["rank"])]

    # ------------------------------------------------------------------
    # Internal helpers (stubs — replace with LLM calls in production)
    # ------------------------------------------------------------------

    def _derive_requirements(self, goal: str, success_conditions: List[str]) -> List[Dict[str, Any]]:
        """
        Stub: In production this calls an LLM to decompose the goal into
        concrete information requirements with source preferences.
        """
        keywords = goal.lower().split()
        base_query = " ".join(keywords[:6]) if len(keywords) > 6 else goal

        requirements = [
            {
                "rank": 1,
                "priority": "high",
                "query": f"{base_query} overview 2026",
                "source_type": "web_search",
                "rationale": "Establish current baseline understanding",
            },
            {
                "rank": 2,
                "priority": "high",
                "query": f"{base_query} latest developments",
                "source_type": "news_search",
                "rationale": "Capture recent news and updates",
            },
            {
                "rank": 3,
                "priority": "medium",
                "query": f"{base_query} research papers",
                "source_type": "academic_search",
                "rationale": "Ground findings in peer-reviewed sources",
            },
        ]

        for condition in success_conditions:
            requirements.append({
                "rank": len(requirements) + 1,
                "priority": "medium",
                "query": f"{base_query} {condition.lower()}",
                "source_type": "web_search",
                "rationale": f"Satisfy success condition: {condition}",
            })

        return requirements

    def _identify_gaps(self, goal: str) -> List[str]:
        """Stub: returns known unknowns about the goal domain."""
        return [
            "Real-time data may be unavailable",
            "Some sources may require paywalled access",
        ]
