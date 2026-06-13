"""
InfoNeedsAgent
==============
Determines what specific information is required to satisfy a clarified goal.

Sits between UserIntentAgent and the iterative search loop. Takes a clarified
goal and success conditions, then outputs a diverse set of concrete information
requirements covering multiple query angles.

Query angles drawn from SOTA research (2025-2026):
- Overview / baseline (what/how)
- Recent developments (news, 2026)
- Step-back abstraction (Google Brain "Take a Step Back")
- Comparison / best practices
- Limitations / challenges (adversarial angle)
- Deep-dive per success condition
- HyDE-style priming (hypothetical ideal answer → drives embedding search)

Reference: "A Survey of Query Optimization in Large Language Models"
           arXiv:2412.17558 — covers decomposition, HyDE, step-back, FLARE
"""

from src.agents.base_agent import BaseAgent
from typing import List, Dict, Any
from datetime import date


CURRENT_YEAR = date.today().year


class InfoNeedsAgent(BaseAgent):
    """
    Decomposes a clarified goal into a rich, multi-angle query set before
    the iterative search loop begins.

    In production, _derive_requirements() sends the goal to an LLM
    (claude-sonnet recommended for reasoning quality) and parses structured
    JSON back. The stubs below implement the same multi-angle strategy
    deterministically so the pipeline runs without live API calls.
    """

    def __init__(self, name: str, model_name: str):
        super().__init__(name, model_name)
        self.info_requirements: List[Dict[str, Any]] = []
        self.knowledge_gaps: List[str] = []
        self.hyde_primer: str = ""  # hypothetical ideal answer for embedding retrieval

    def act(self, clarified_goal: str, success_conditions: List[str] = None) -> str:
        """
        Analyzes the clarified goal and returns structured information requirements.

        Structured data is also available via self.info_requirements,
        self.knowledge_gaps, and self.hyde_primer after this call.
        """
        print(f"{self.name} (InfoNeeds) decomposing requirements for: {clarified_goal}")

        self.info_requirements = self._derive_requirements(clarified_goal, success_conditions or [])
        self.knowledge_gaps = self._identify_initial_gaps(clarified_goal)
        self.hyde_primer = self._generate_hyde_primer(clarified_goal)

        summary_lines = [f"Query decomposition for: {clarified_goal}"]
        for req in self.info_requirements:
            summary_lines.append(
                f"  [{req['priority'].upper():6s}] [{req['angle']:12s}] {req['query']}"
            )
        if self.knowledge_gaps:
            summary_lines.append(f"Initial gaps flagged: {', '.join(self.knowledge_gaps)}")

        return "\n".join(summary_lines)

    def plan(self, task: str) -> List[str]:
        return [
            "Parse clarified goal into core topic + modifiers",
            "Generate overview query for baseline understanding",
            "Generate recency query (temporally anchored to current year)",
            "Generate step-back abstraction query for broader context",
            "Generate comparison / best-practices query",
            "Generate limitations / challenges query (adversarial angle)",
            "Generate one deep-dive query per success condition",
            "Flag known access/recency gaps upfront",
            "Produce HyDE primer for semantic embedding retrieval",
        ]

    def get_search_queries(self) -> List[str]:
        """Returns queries ordered by rank (high-priority angles first)."""
        return [r["query"] for r in sorted(self.info_requirements, key=lambda x: x["rank"])]

    def get_requirements_by_source(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups requirements by source_type for parallel dispatch."""
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for req in self.info_requirements:
            grouped.setdefault(req["source_type"], []).append(req)
        return grouped

    # ------------------------------------------------------------------
    # Internal helpers (stubs — replace with LLM calls in production)
    # ------------------------------------------------------------------

    def _derive_requirements(self, goal: str, success_conditions: List[str]) -> List[Dict[str, Any]]:
        """
        Generates a diverse, multi-angle query set.

        Angles used (following FAIR-RAG checklist pattern and step-back prompting):
          1. overview      — broad baseline (what is X, how does X work)
          2. recency       — temporally anchored to current year, news-focused
          3. step_back     — abstract/parent topic for broader retrieval context
          4. best_practice — comparative / "best approaches" framing
          5. challenges    — adversarial angle: what doesn't work, limitations
          Per success condition: targeted deep-dive
        """
        topic = self._extract_topic(goal)
        rank = 1
        reqs: List[Dict[str, Any]] = []

        def add(angle: str, priority: str, query: str, source: str, rationale: str):
            nonlocal rank
            reqs.append({
                "rank": rank,
                "angle": angle,
                "priority": priority,
                "query": query,
                "source_type": source,
                "rationale": rationale,
            })
            rank += 1

        # 1. Overview — broad baseline
        add("overview", "high",
            f"{topic} overview {CURRENT_YEAR}",
            "web_search",
            "Establish baseline understanding of the topic")

        # 2. Recency — temporally anchored, news-focused
        add("recency", "high",
            f"{topic} latest developments {CURRENT_YEAR} new",
            "news_search",
            "Capture the most recent news, releases, and updates")

        # 3. Step-back — broader/parent context (Google Brain pattern)
        step_back_topic = self._step_back(topic)
        add("step_back", "high",
            f"{step_back_topic} principles fundamentals",
            "web_search",
            "Retrieve broader context to ground specific findings (step-back prompting)")

        # 4. Best practices / comparison
        add("best_practice", "medium",
            f"best {topic} approaches comparison {CURRENT_YEAR}",
            "web_search",
            "Find comparative analysis and consensus best practices")

        # 5. Limitations / challenges (adversarial angle)
        add("challenges", "medium",
            f"{topic} challenges limitations pitfalls {CURRENT_YEAR}",
            "web_search",
            "Understand failure modes and open problems (adversarial coverage)")

        # 6. Academic depth
        add("academic", "medium",
            f"{topic} research paper {CURRENT_YEAR} study",
            "academic_search",
            "Ground findings in peer-reviewed or preprint sources")

        # 7. Per success condition — targeted deep-dive
        for condition in success_conditions:
            add("success_cond", "high",
                f"{topic} {condition.lower()} {CURRENT_YEAR}",
                "web_search",
                f"Directly address success criterion: '{condition}'")

        return reqs

    def _extract_topic(self, goal: str) -> str:
        """
        Strips question words to get the core topic phrase.
        Production version uses NLP/LLM for proper noun-phrase extraction.
        """
        stop_words = {
            "what", "are", "the", "best", "how", "do", "i", "can", "we",
            "is", "a", "an", "of", "for", "in", "and", "or", "to", "tell",
            "me", "about", "explain", "describe", "find", "list", "give",
        }
        import re
        clean = re.sub(r"[^\w\s]", "", goal.lower())
        words = [w for w in clean.split() if w not in stop_words]
        return " ".join(words[:7]) if words else goal

    def _step_back(self, topic: str) -> str:
        """
        Generates an abstracted/parent topic for step-back prompting.
        Production version uses an LLM to generate a genuine abstraction.
        E.g., "RAG architectures for production LLMs" → "retrieval augmented generation"
        """
        words = topic.split()
        if len(words) > 3:
            return " ".join(words[:3])
        return topic

    def _generate_hyde_primer(self, goal: str) -> str:
        """
        HyDE (Hypothetical Document Embeddings): generates a short passage
        describing what an ideal answer would contain.

        In production: prompt an LLM with "Write a 2-sentence passage that
        directly answers: {goal}" — the passage is encoded as a dense vector
        for embedding-based retrieval (not used for factual grounding).

        Reference: Gao et al. 2022; HyPE extension (Vake et al. SSRN:5139335)
        """
        return (
            f"An ideal answer to '{goal}' would cover: the current state of "
            f"the field as of {CURRENT_YEAR}, key methodologies and tools, "
            f"comparison of leading approaches, known limitations, and "
            f"actionable recommendations based on recent evidence."
        )

    def _identify_initial_gaps(self, goal: str) -> List[str]:
        """Pre-flags known access/recency constraints before any search runs."""
        return [
            f"Real-time data beyond {CURRENT_YEAR} may be unavailable",
            "Paywalled academic sources may require institutional access",
            "Proprietary systems (OpenAI, Google, etc.) may have undisclosed internals",
        ]
