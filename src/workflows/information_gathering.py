"""
Information Gathering Workflow
==============================
Use case: the user wants to find / learn about a topic.

Pipeline
--------
1. UserIntentAgent    — clarify goal and success conditions
2. InfoNeedsAgent     — determine what specific information is required
3. OrchestratorAgent  — build a ranked search plan from requirements
4. InfoGatheringAgent — execute searches and synthesize results
5. Output             — return structured result (store later via ObsidianAgent etc.)

Each phase receives the output of the previous one, so context accumulates
through the pipeline rather than being re-derived at each step.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

from src.agents.user_intent_agent import UserIntentDiscoveryAgent
from src.agents.info_needs_agent import InfoNeedsAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.agents.info_gathering_agent import InfoGatheringAgent


@dataclass
class GatheringResult:
    """Carries the accumulated context through the pipeline."""
    original_query: str
    clarified_goal: str = ""
    success_conditions: List[str] = field(default_factory=list)
    info_requirements: List[Dict[str, Any]] = field(default_factory=list)
    knowledge_gaps: List[str] = field(default_factory=list)
    search_plan: List[Dict[str, Any]] = field(default_factory=list)
    gathered_results: List[Dict[str, str]] = field(default_factory=list)
    final_summary: str = ""
    needs_clarification: bool = False


class InformationGatheringWorkflow:
    """
    Orchestrates the end-to-end information gathering pipeline.

    Each agent can be swapped for a different model or implementation.
    Intended usage:

        workflow = InformationGatheringWorkflow()
        result = workflow.run("What are the best practices for RAG in 2026?")
        print(result.final_summary)
    """

    def __init__(
        self,
        intent_model: str = "claude-haiku-4-5-20251001",
        needs_model: str = "claude-sonnet-4-6",
        orchestrator_model: str = "claude-sonnet-4-6",
        gathering_model: str = "claude-haiku-4-5-20251001",
    ):
        self.intent_agent = UserIntentDiscoveryAgent(
            name="Intent", model_name=intent_model
        )
        self.needs_agent = InfoNeedsAgent(
            name="InfoNeeds", model_name=needs_model
        )
        self.orchestrator = OrchestratorAgent(
            name="Strategist", model_name=orchestrator_model
        )
        self.gathering_agent = InfoGatheringAgent(
            name="Researcher", model_name=gathering_model
        )

    def run(self, user_query: str) -> GatheringResult:
        result = GatheringResult(original_query=user_query)

        # ── Phase 1: Understand what the user wants ──────────────────────
        print("\n[Phase 1] User Intent Discovery")
        intent_response = self.intent_agent.act(user_query)
        print(f"  → {intent_response}")

        if "vague" in intent_response.lower():
            result.needs_clarification = True
            result.clarified_goal = user_query
            return result

        result.clarified_goal = getattr(self.intent_agent, "clarified_goal", user_query)
        result.success_conditions = getattr(self.intent_agent, "success_conditions", [])

        # ── Phase 2: Determine what information is needed ────────────────
        print("\n[Phase 2] Information Needs Analysis")
        needs_response = self.needs_agent.act(result.clarified_goal, result.success_conditions)
        print(f"  → {needs_response}")

        result.info_requirements = self.needs_agent.info_requirements
        result.knowledge_gaps = self.needs_agent.knowledge_gaps
        search_queries = self.needs_agent.get_search_queries()

        # ── Phase 3: Build a search plan ─────────────────────────────────
        print("\n[Phase 3] Orchestration & Search Planning")
        self.orchestrator.act(result.clarified_goal)
        result.search_plan = self._build_search_plan(search_queries)
        print(f"  → {len(result.search_plan)} queries planned")

        # ── Phase 4: Execute searches ─────────────────────────────────────
        print("\n[Phase 4] Information Gathering")
        gathered = []
        for item in result.search_plan:
            query = item["query"]
            print(f"  Searching: {query}")
            raw = self.gathering_agent.act(query)
            gathered.append({"query": query, "result": raw})

        result.gathered_results = gathered

        # ── Phase 5: Synthesize ───────────────────────────────────────────
        print("\n[Phase 5] Synthesis")
        result.final_summary = self._synthesize(result)
        print(f"  → Summary ready ({len(result.final_summary)} chars)")

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_search_plan(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Converts flat query list into a ranked execution plan."""
        return [
            {"rank": i + 1, "query": q, "status": "pending"}
            for i, q in enumerate(queries)
        ]

    def _synthesize(self, result: GatheringResult) -> str:
        """
        Stub synthesizer. In production, pass all gathered_results back
        through an LLM to produce a coherent final answer.
        """
        lines = [
            f"Goal: {result.clarified_goal}",
            f"Success criteria: {', '.join(result.success_conditions)}",
            "",
            "Findings:",
        ]
        for item in result.gathered_results:
            lines.append(f"  [{item['query']}]")
            lines.append(f"    {item['result']}")

        if result.knowledge_gaps:
            lines.append("")
            lines.append(f"Known gaps: {', '.join(result.knowledge_gaps)}")

        return "\n".join(lines)
