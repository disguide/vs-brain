"""
GapAnalysisAgent
================
Implements the core SOTA pattern from Perplexity Deep Research and the
qx-labs/agents-deep-research architecture: after each search iteration,
assess what's still missing and decide whether to continue searching.

Based on:
- Perplexity's iterative agentic RAG loop (search → gaps → re-search)
- Knowledge Gap Agent pattern (https://github.com/qx-labs/agents-deep-research)
- CRAG-MoW (Corrective RAG - Mixture of Workflows) completeness verification
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

from src.agents.base_agent import BaseAgent


@dataclass
class GapAnalysisResult:
    """Output of a single gap analysis pass."""
    is_sufficient: bool
    confidence_score: float          # 0.0–1.0; exit loop at >= threshold
    covered_aspects: List[str]
    gaps: List[str]
    follow_up_queries: List[Dict[str, str]]  # [{query, source_type, gap_addressed}]
    reasoning: str


class GapAnalysisAgent(BaseAgent):
    """
    After each search iteration, evaluates coverage against the original goal
    and success conditions, then decides:
      - Is the accumulated information sufficient to synthesize a good answer?
      - If not, what specific gaps remain?
      - What targeted follow-up queries will close those gaps?

    In production, the analyze() call passes the full goal + all gathered
    content to an LLM (claude-sonnet recommended) which returns structured JSON.
    The stubs below simulate that logic deterministically.
    """

    SUFFICIENCY_THRESHOLD = 0.80  # confidence score to stop iterating

    def __init__(self, name: str, model_name: str):
        super().__init__(name, model_name)
        self.last_result: GapAnalysisResult | None = None

    def act(self, task: str) -> str:
        return f"{self.name} ready to analyze gaps for: {task}"

    def plan(self, task: str) -> List[str]:
        return [
            "Review accumulated results against goal",
            "Identify which success conditions are covered",
            "List remaining knowledge gaps",
            "Generate targeted follow-up queries per gap",
            "Score overall confidence",
        ]

    def analyze(
        self,
        goal: str,
        success_conditions: List[str],
        results: List[Dict[str, Any]],
        running_summary: str,
        iteration: int,
    ) -> GapAnalysisResult:
        """
        Core method. Called after every search iteration.

        In production: sends goal + success_conditions + running_summary to an
        LLM and parses structured JSON back. Here we stub it with a heuristic
        that scales confidence with iteration count and result volume so the
        demo loop terminates sensibly.
        """
        print(f"  {self.name} analyzing gaps (iteration {iteration}, {len(results)} results so far)")

        covered, gaps = self._assess_coverage(goal, success_conditions, results)

        confidence = self._score_confidence(covered, success_conditions, results, iteration)
        is_sufficient = confidence >= self.SUFFICIENCY_THRESHOLD

        follow_up_queries = [] if is_sufficient else self._generate_follow_ups(goal, gaps, iteration)

        reasoning = (
            f"Iteration {iteration}: {len(covered)}/{len(success_conditions)} "
            f"success conditions covered. Confidence {confidence:.1%}."
        )

        self.last_result = GapAnalysisResult(
            is_sufficient=is_sufficient,
            confidence_score=confidence,
            covered_aspects=covered,
            gaps=gaps,
            follow_up_queries=follow_up_queries,
            reasoning=reasoning,
        )
        return self.last_result

    # ------------------------------------------------------------------
    # Internal helpers (stubs — replace with LLM calls in production)
    # ------------------------------------------------------------------

    def _assess_coverage(
        self, goal: str, success_conditions: List[str], results: List[Dict[str, Any]]
    ):
        """
        Stub: checks which success conditions are addressed by gathered results.
        Production version passes content to an LLM for semantic matching.
        """
        result_text = " ".join(r.get("content", r.get("result", "")) for r in results).lower()

        covered = []
        gaps = []
        for condition in success_conditions:
            keywords = condition.lower().split()
            if any(kw in result_text for kw in keywords):
                covered.append(condition)
            else:
                gaps.append(f"Missing coverage for: {condition}")

        # Always surface topic-level gaps based on goal keywords
        goal_keywords = set(goal.lower().split()) - {"the", "a", "an", "of", "for", "in", "and", "or", "to"}
        uncovered_topics = [kw for kw in list(goal_keywords)[:3] if kw not in result_text]
        if uncovered_topics:
            gaps.append(f"Goal aspects not yet found: {', '.join(uncovered_topics)}")

        return covered, gaps

    def _score_confidence(
        self,
        covered: List[str],
        success_conditions: List[str],
        results: List[Dict[str, Any]],
        iteration: int,
    ) -> float:
        """
        Stub confidence scorer. Production version uses an LLM rubric.
        Factors: condition coverage, result volume, iteration depth.
        """
        if not success_conditions:
            base = 0.5
        else:
            base = len(covered) / len(success_conditions)

        # Reward more results (up to a ceiling) and deeper iterations
        volume_bonus = min(len(results) * 0.04, 0.20)
        depth_bonus = min(iteration * 0.08, 0.24)

        return min(base + volume_bonus + depth_bonus, 1.0)

    def _generate_follow_ups(
        self, goal: str, gaps: List[str], iteration: int
    ) -> List[Dict[str, str]]:
        """
        Stub: generates targeted follow-up queries for remaining gaps.
        Production version has the LLM craft precise queries per gap.
        """
        queries = []
        source_cycle = ["web_search", "news_search", "academic_search"]

        for i, gap in enumerate(gaps[:3]):  # cap at 3 follow-ups per iteration
            # Extract the core topic from the gap description
            topic = gap.replace("Missing coverage for:", "").replace("Goal aspects not yet found:", "").strip()
            queries.append({
                "query": f"{goal} {topic} depth analysis 2026",
                "source_type": source_cycle[i % len(source_cycle)],
                "gap_addressed": gap,
            })

        return queries
