"""
InfoGatheringAgent
==================
Executes individual search queries and returns structured, scored results.

Key SOTA practices implemented:
- Structured SearchResult with relevance scoring (CRAG pattern)
- Source-type routing (web / news / academic / url_extraction)
- Temporal anchoring — current date injected into all queries
- Parallel-ready interface (act_structured returns one result per call;
  the workflow layer decides whether to fan out in parallel)

Reference: Perplexity's 6-stage RAG pipeline (BM25 + dense + 3-tier reranker)
           arXiv:2401.15884 CRAG — relevance scoring before generation
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Any

from src.agents.base_agent import BaseAgent


CURRENT_DATE = date.today().isoformat()
CURRENT_YEAR = date.today().year


@dataclass
class SearchResult:
    """
    Structured result from a single search execution.

    relevance_score: 0.0–1.0 estimate of how well the content addresses the query.
                     In production: use a cross-encoder reranker (CRAG pattern).
    iteration:       which loop iteration produced this result (for provenance).
    source_url:      populated when source_type == "url_extraction".
    """
    query: str
    content: str
    source_type: str
    relevance_score: float
    iteration: int
    source_url: str = ""


class InfoGatheringAgent(BaseAgent):
    """
    Executes search queries via registered tools and returns SearchResult objects.

    Tool routing by source_type:
      web_search      → broad web retrieval (BM25 + dense hybrid)
      news_search     → recency-focused news index
      academic_search → preprint / paper search (arXiv, Semantic Scholar)
      url_extraction  → targeted deep extraction from a known URL

    In production: each route calls the corresponding tool registered on the
    AgentHarness. Results are scored by a lightweight cross-encoder before
    being returned (CRAG-style relevance evaluation).
    """

    def __init__(self, name: str, model_name: str):
        super().__init__(name, model_name)

    def act(self, task: str) -> str:
        """Compatibility wrapper — delegates to act_structured."""
        result = self.act_structured(task, source_type="web_search", iteration=1)
        return result.content

    def act_structured(
        self,
        query: str,
        source_type: str = "web_search",
        iteration: int = 1,
    ) -> SearchResult:
        """
        Core method. Executes a single search and returns a scored result.

        Steps (production implementation):
          1. Anchor query to current date to defeat training-cutoff staleness
          2. Route to the appropriate search tool via the harness
          3. Score relevance with a cross-encoder (CRAG pattern)
          4. Return structured SearchResult

        The stub below simulates steps 1 and 4; steps 2-3 require live tools.
        """
        anchored_query = self._anchor_query(query, source_type)
        print(f"  {self.name} [{source_type}] iter={iteration}: {anchored_query}")

        # Production: harness.execute_tool(source_type, anchored_query)
        content = self._stub_search(anchored_query, source_type)

        # Production: cross-encoder reranker scores content vs original query
        relevance = self._stub_relevance_score(query, content, iteration)

        return SearchResult(
            query=anchored_query,
            content=content,
            source_type=source_type,
            relevance_score=relevance,
            iteration=iteration,
        )

    def plan(self, task: str) -> List[str]:
        return [
            "Anchor query with current date to ensure recency",
            "Route to appropriate search tool (web/news/academic/url)",
            "Execute search and retrieve raw results",
            "Score relevance with cross-encoder (CRAG pattern)",
            "Return structured SearchResult",
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _anchor_query(self, query: str, source_type: str) -> str:
        """
        Temporal anchoring: ensures all queries reference the current period.

        News searches get an explicit date; academic searches get year + "preprint".
        Web searches get the year appended if not already present.

        This addresses the most common SOTA failure: LLM-assisted searches
        defaulting to stale training-data results rather than current content.
        """
        year_str = str(CURRENT_YEAR)

        if source_type == "news_search":
            if year_str not in query:
                return f"{query} {CURRENT_DATE}"
            return query

        if source_type == "academic_search":
            suffix = f"{CURRENT_YEAR} preprint" if year_str not in query else "preprint"
            return f"{query} {suffix}"

        # web_search and url_extraction
        if year_str not in query and str(CURRENT_YEAR - 1) not in query:
            return f"{query} {CURRENT_YEAR}"
        return query

    def _stub_search(self, query: str, source_type: str) -> str:
        """
        Stub: simulates search tool output.
        Production: calls the registered tool via AgentHarness.execute_tool().
        """
        source_labels = {
            "web_search": "Web",
            "news_search": "News",
            "academic_search": "Academic",
            "url_extraction": "URL",
        }
        label = source_labels.get(source_type, source_type)
        return (
            f"[{label} result for: {query}] "
            f"Comprehensive findings as of {CURRENT_DATE}. "
            f"Production implementation replaces this with live tool output "
            f"from the registered {source_type} tool on AgentHarness."
        )

    def _stub_relevance_score(self, original_query: str, content: str, iteration: int) -> float:
        """
        Stub: simulates CRAG-style cross-encoder relevance scoring.
        Production: passes (original_query, content) to a cross-encoder model.
        Score represents P(content is relevant to query).
        Stub increases with iteration depth (deeper iterations yield better targeted results).
        """
        base = 0.60
        depth_bonus = min(iteration * 0.08, 0.24)
        return round(min(base + depth_bonus, 0.98), 2)
