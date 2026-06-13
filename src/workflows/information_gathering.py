"""
Information Gathering Workflow
==============================
Use case: the user wants to find, learn about, or research a topic.

Pipeline
--------
1. UserIntentAgent    — clarify goal and success conditions
2. InfoNeedsAgent     — multi-angle query decomposition (overview, recency,
                        step-back, best-practice, challenges, per-condition)
3. Iterative Search Loop (SOTA):
   ├─ 3a. Fan out searches across source types (web/news/academic)
   ├─ 3b. GapAnalysisAgent — what's still missing? confidence score?
   ├─ 3c. If not sufficient: generate follow-up queries and loop
   └─ 3d. Exit when confident ≥ threshold or max_iterations reached
4. Final Synthesis     — structured summary with provenance and gap report

Key SOTA patterns implemented:
- Iterative search loop with gap detection (Perplexity Deep Research pattern,
  qx-labs/agents-deep-research, FAIR-RAG checklist approach)
- Multi-angle query decomposition (step-back prompting, HyDE primer, 6 angles)
- Structured SearchResult with relevance scoring (CRAG-style evaluation)
- Running intermediate summary carried between iterations
- Explicit confidence/sufficiency scoring before exit
- Source-type routing (web / news / academic)
- Temporal anchoring on all queries (defeat LLM training-cutoff staleness)

References:
- Perplexity Sonar Deep Research architecture: 20–50 queries, iterative loop
- OpenAI Deep Research: RL-trained plan-search-reflect-synthesize loop
- FAIR-RAG (arXiv:2510.22344): checklist-driven gap detection
- qx-labs/agents-deep-research: Knowledge Gap Agent pattern
- CRAG (arXiv:2401.15884): relevance scoring before synthesis
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

from src.agents.user_intent_agent import UserIntentDiscoveryAgent
from src.agents.info_needs_agent import InfoNeedsAgent
from src.agents.info_gathering_agent import InfoGatheringAgent, SearchResult
from src.agents.gap_analysis_agent import GapAnalysisAgent


@dataclass
class IterationStats:
    """Records what happened during one search iteration."""
    iteration: int
    queries_run: int
    new_results: int
    confidence_score: float
    gaps_remaining: List[str]
    is_sufficient: bool


@dataclass
class GatheringResult:
    """
    Carries the accumulated context through the full pipeline.
    Designed to be passed directly to downstream agents (Obsidian, Verifier, etc.)
    """
    original_query: str
    clarified_goal: str = ""
    success_conditions: List[str] = field(default_factory=list)
    hyde_primer: str = ""
    info_requirements: List[Dict[str, Any]] = field(default_factory=list)
    initial_gaps: List[str] = field(default_factory=list)

    # Search phase — populated by the iterative loop
    all_results: List[SearchResult] = field(default_factory=list)
    iteration_stats: List[IterationStats] = field(default_factory=list)
    final_confidence: float = 0.0
    total_iterations: int = 0

    # Output
    running_summary: str = ""
    final_summary: str = ""
    needs_clarification: bool = False


class InformationGatheringWorkflow:
    """
    Orchestrates the end-to-end information gathering pipeline.

    Default model assignments follow the SOTA cost-optimization pattern:
    - Fast/cheap model (haiku) for high-volume I/O steps
    - Capable model (sonnet) for planning, reasoning, and gap analysis

    Usage:
        workflow = InformationGatheringWorkflow()
        result = workflow.run("What are the best RAG architectures in 2026?")
        print(result.final_summary)
    """

    MAX_ITERATIONS = 3

    def __init__(
        self,
        intent_model: str = "claude-haiku-4-5-20251001",
        needs_model: str = "claude-sonnet-4-6",
        gathering_model: str = "claude-haiku-4-5-20251001",
        gap_model: str = "claude-sonnet-4-6",
    ):
        self.intent_agent = UserIntentDiscoveryAgent(
            name="Intent", model_name=intent_model
        )
        self.needs_agent = InfoNeedsAgent(
            name="InfoNeeds", model_name=needs_model
        )
        self.gathering_agent = InfoGatheringAgent(
            name="Researcher", model_name=gathering_model
        )
        self.gap_agent = GapAnalysisAgent(
            name="GapAnalyzer", model_name=gap_model
        )

    def run(self, user_query: str) -> GatheringResult:
        result = GatheringResult(original_query=user_query)

        # ── Phase 1: Clarify what the user wants ─────────────────────────
        print("\n[Phase 1] User Intent Discovery")
        intent_response = self.intent_agent.act(user_query)
        print(f"  → {intent_response}")

        if "vague" in intent_response.lower():
            result.needs_clarification = True
            result.clarified_goal = user_query
            return result

        result.clarified_goal = getattr(self.intent_agent, "clarified_goal", user_query)
        result.success_conditions = getattr(self.intent_agent, "success_conditions", [])

        # ── Phase 2: Multi-angle query decomposition ──────────────────────
        print("\n[Phase 2] Information Needs Decomposition")
        needs_response = self.needs_agent.act(result.clarified_goal, result.success_conditions)
        print(f"  → {needs_response}")

        result.info_requirements = self.needs_agent.info_requirements
        result.initial_gaps = self.needs_agent.knowledge_gaps
        result.hyde_primer = self.needs_agent.hyde_primer

        # Build initial query queue from requirements
        current_queries = [
            {"query": r["query"], "source_type": r["source_type"]}
            for r in self.needs_agent.info_requirements
        ]
        print(f"  → {len(current_queries)} initial queries across "
              f"{len(self.needs_agent.get_requirements_by_source())} source types")

        # ── Phase 3: Iterative search loop ───────────────────────────────
        # Pattern: search → assess gaps → re-search until sufficient
        # Based on: Perplexity Deep Research, FAIR-RAG, qx-labs/agents-deep-research
        print("\n[Phase 3] Iterative Search Loop (SOTA)")

        iteration = 0
        while iteration < self.MAX_ITERATIONS:
            iteration += 1
            print(f"\n  ── Iteration {iteration}/{self.MAX_ITERATIONS} "
                  f"({len(current_queries)} queries) ──")

            # 3a. Execute all queries for this iteration
            # Production: fan out in parallel with asyncio.gather() or
            # a thread pool; sequential here for stub compatibility
            iteration_results: List[SearchResult] = []
            for item in current_queries:
                search_result = self.gathering_agent.act_structured(
                    query=item["query"],
                    source_type=item["source_type"],
                    iteration=iteration,
                )
                iteration_results.append(search_result)

            result.all_results.extend(iteration_results)

            # 3b. Update running summary with new findings
            result.running_summary = self._update_running_summary(
                result.running_summary, iteration_results, iteration
            )

            # 3c. Gap analysis — what's still missing? Are we confident enough?
            gap_result = self.gap_agent.analyze(
                goal=result.clarified_goal,
                success_conditions=result.success_conditions,
                results=[{"content": r.content, "query": r.query} for r in result.all_results],
                running_summary=result.running_summary,
                iteration=iteration,
            )

            stats = IterationStats(
                iteration=iteration,
                queries_run=len(current_queries),
                new_results=len(iteration_results),
                confidence_score=gap_result.confidence_score,
                gaps_remaining=gap_result.gaps,
                is_sufficient=gap_result.is_sufficient,
            )
            result.iteration_stats.append(stats)

            print(f"  Confidence: {gap_result.confidence_score:.0%} | "
                  f"Covered: {len(gap_result.covered_aspects)}/{len(result.success_conditions)} | "
                  f"Gaps: {len(gap_result.gaps)}")
            print(f"  {gap_result.reasoning}")

            # 3d. Exit conditions
            if gap_result.is_sufficient:
                print(f"  ✓ Sufficient — exiting loop after {iteration} iteration(s)")
                break

            if not gap_result.follow_up_queries:
                print("  No follow-up queries generated — exiting loop")
                break

            # 3e. Prepare follow-up queries for next iteration
            current_queries = gap_result.follow_up_queries
            print(f"  → {len(current_queries)} follow-up queries targeting remaining gaps")

        result.total_iterations = iteration
        result.final_confidence = (
            result.iteration_stats[-1].confidence_score if result.iteration_stats else 0.0
        )

        # ── Phase 4: Final synthesis ──────────────────────────────────────
        print("\n[Phase 4] Synthesis")
        result.final_summary = self._synthesize(result)
        print(f"  → Summary ready ({len(result.final_summary)} chars, "
              f"{len(result.all_results)} sources, "
              f"{result.total_iterations} iteration(s), "
              f"confidence {result.final_confidence:.0%})")

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _update_running_summary(
        self,
        current_summary: str,
        new_results: List[SearchResult],
        iteration: int,
    ) -> str:
        """
        Builds a running intermediate summary after each iteration.

        Production: pass current_summary + new_results to an LLM for
        coherent incremental synthesis. The stub concatenates structured
        excerpts so downstream agents can detect coverage without an LLM call.

        This mirrors Gemini Deep Research's "ground on all information gathered
        so far" step at the end of each iteration.
        """
        new_block = f"\n--- Iteration {iteration} findings ---\n"
        for r in new_results:
            if r.relevance_score >= 0.60:  # filter low-relevance results
                new_block += f"[{r.source_type}] {r.query}\n  {r.content[:200]}...\n"
        return current_summary + new_block

    def _synthesize(self, result: GatheringResult) -> str:
        """
        Produces the final structured summary.

        Production: pass all_results + running_summary + goal + success_conditions
        to an LLM for coherent, cited synthesis. Mirrors OpenAI Deep Research's
        final "write a cited report" synthesis step.
        """
        lines = [
            f"# Research Summary",
            f"Goal: {result.clarified_goal}",
            f"Iterations: {result.total_iterations} | "
            f"Sources searched: {len(result.all_results)} | "
            f"Confidence: {result.final_confidence:.0%}",
            "",
            f"Success criteria: {', '.join(result.success_conditions)}",
            "",
            "## Findings by source type",
        ]

        # Group by source_type for readability
        by_source: Dict[str, List[SearchResult]] = {}
        for r in result.all_results:
            by_source.setdefault(r.source_type, []).append(r)

        for source_type, results in by_source.items():
            lines.append(f"\n### {source_type.replace('_', ' ').title()}")
            for r in results:
                lines.append(
                    f"  [iter {r.iteration} | relevance {r.relevance_score:.2f}] {r.query}"
                )
                lines.append(f"    {r.content[:300]}")

        # Iteration-by-iteration confidence progression
        if result.iteration_stats:
            lines.append("\n## Search Progression")
            for stat in result.iteration_stats:
                lines.append(
                    f"  Iter {stat.iteration}: {stat.queries_run} queries → "
                    f"confidence {stat.confidence_score:.0%}"
                    + (" ✓ sufficient" if stat.is_sufficient else f" | gaps: {len(stat.gaps_remaining)}")
                )

        # Residual gaps
        final_gaps = result.iteration_stats[-1].gaps_remaining if result.iteration_stats else result.initial_gaps
        if final_gaps:
            lines.append("\n## Remaining gaps (for follow-up)")
            for gap in final_gaps:
                lines.append(f"  - {gap}")

        if result.hyde_primer:
            lines.append(f"\n## HyDE primer used for embedding retrieval")
            lines.append(f"  {result.hyde_primer}")

        return "\n".join(lines)
