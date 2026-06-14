import type { EdgeType, Graph, GraphNode } from "../data/types";
import { getChildren, isFullyGrounded } from "../lib/graph";

interface NodeCardProps {
  graph: Graph;
  node: GraphNode;
  /** The edge type by which this node was reached from its parent (root: none). */
  viaEdge?: EdgeType;
  expanded: boolean;
  onToggle: () => void;
}

// Short, human label shown in the corner of each card.
function typeLabel(node: GraphNode): string {
  switch (node.type) {
    case "question":
      return "QUESTION";
    case "position":
      return "POSITION";
    case "argument":
      return node.stance === "attack" ? "ATTACKS" : "SUPPORTS";
    case "value":
      return "BEDROCK VALUE";
  }
}

// The leading marker/icon for each node type.
function typeMarker(node: GraphNode): string {
  switch (node.type) {
    case "question":
      return "?";
    case "position":
      return "▸";
    case "argument":
      return node.stance === "attack" ? "✕" : "✓";
    case "value":
      return "⚓"; // anchor = you've hit the bottom
  }
}

/**
 * Renders a single node, styled by type. Purely presentational — expand/collapse
 * state is owned by the TreeView.
 */
export function NodeCard({
  graph,
  node,
  viaEdge,
  expanded,
  onToggle,
}: NodeCardProps) {
  const children = getChildren(graph, node.id);
  const hasChildren = children.length > 0;
  const isValue = node.type === "value";
  const isShared = viaEdge === "shared-value";

  // Class drives the colour scheme (see styles.css).
  const variant =
    node.type === "argument" ? `argument-${node.stance ?? "support"}` : node.type;

  return (
    <button
      type="button"
      className={`card card-${variant}${isValue ? " card-terminal" : ""}`}
      onClick={isValue ? undefined : onToggle}
      // Value nodes are terminal; nothing to expand.
      aria-expanded={isValue ? undefined : expanded}
      data-clickable={!isValue}
    >
      <div className="card-head">
        <span className="card-marker" aria-hidden="true">
          {typeMarker(node)}
        </span>
        <span className="card-tag">{typeLabel(node)}</span>

        {node.type === "question" && (
          <span
            className={`badge ${
              isFullyGrounded(graph, node.id) ? "badge-grounded" : "badge-open"
            }`}
          >
            {isFullyGrounded(graph, node.id) ? "FULLY GROUNDED" : "OPEN"}
          </span>
        )}

        {isShared && (
          <span className="badge badge-shared" title="Value reused across questions">
            ↺ shared
          </span>
        )}

        {!isValue && hasChildren && (
          <span className="card-chevron" aria-hidden="true">
            {expanded ? "▾" : "▸"}
          </span>
        )}
      </div>

      <div className="card-content">{node.content}</div>

      {isValue && (
        <div className="card-terminal-note">Terminal — a chain bottoms out here.</div>
      )}
    </button>
  );
}
