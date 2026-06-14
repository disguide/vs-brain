import type { EdgeType, Graph, GraphNode } from "../data/types";

// A tree-child of a node, plus the edge type that connects them.
export interface ChildLink {
  node: GraphNode;
  edgeType: EdgeType;
}

/**
 * Edges are authored in their natural semantic direction, which is not always
 * top-to-bottom in the drill-down tree. This table records, for each edge type,
 * whether the visual *parent* (the node you drill FROM) is the edge's `from`
 * endpoint or its `to` endpoint.
 *
 *   answers      : position -> question   => parent is `to`   (question), child is `from` (position)
 *   supports     : argument -> position   => parent is `to`   (position), child is `from` (argument)
 *   attacks      : argument -> position   => parent is `to`   (position), child is `from` (argument)
 *   raises       : argument -> question   => parent is `from` (argument), child is `to`   (question)
 *   grounds-in   : argument -> value      => parent is `from` (argument), child is `to`   (value)
 *   shared-value : argument -> value      => parent is `from` (argument), child is `to`   (value)
 */
const PARENT_ENDPOINT: Record<EdgeType, "from" | "to"> = {
  answers: "to",
  supports: "to",
  attacks: "to",
  raises: "from",
  "grounds-in": "from",
  "shared-value": "from",
};

export function getNodeById(graph: Graph, id: string): GraphNode | undefined {
  return graph.nodes.find((n) => n.id === id);
}

/**
 * Returns the edge type connecting `from` -> `to`, if such an edge exists.
 * (Direction-sensitive: looks for an edge authored from `from` to `to`.)
 */
export function getEdgeType(
  graph: Graph,
  from: string,
  to: string,
): EdgeType | undefined {
  return graph.edges.find((e) => e.from === from && e.to === to)?.edgeType;
}

/**
 * Returns the tree-children of `nodeId`: the nodes that hang directly beneath it
 * in the drill-down, each paired with the edge type connecting them.
 *
 * Because edges are stored in semantic (not visual) direction, we treat a node
 * as the parent of an edge when it sits on that edge's PARENT_ENDPOINT, and
 * return the node on the opposite endpoint as the child.
 */
export function getChildren(graph: Graph, nodeId: string): ChildLink[] {
  const children: ChildLink[] = [];

  for (const edge of graph.edges) {
    const parentEndpoint = PARENT_ENDPOINT[edge.edgeType];
    const parentId = parentEndpoint === "from" ? edge.from : edge.to;
    if (parentId !== nodeId) continue;

    const childId = parentEndpoint === "from" ? edge.to : edge.from;
    const childNode = getNodeById(graph, childId);
    if (childNode) {
      children.push({ node: childNode, edgeType: edge.edgeType });
    }
  }

  return children;
}

/**
 * True if EVERY argument chain descending from this node eventually reaches a
 * "value" node (via grounds-in or shared-value). False if any branch dead-ends
 * at an unanswered question or a dangling argument.
 *
 * Definitions (all must hold "for every branch"):
 *   - value    : grounded (terminal bedrock).
 *   - argument : grounded iff it has >= 1 child and every child is grounded
 *                (a child value is grounded; a raised question recurses).
 *   - position : grounded iff it has >= 1 argument child and all are grounded.
 *   - question : grounded iff it has >= 1 position child and all are grounded.
 *
 * `visited` guards against cycles — the graph is a DAG, but we stay defensive.
 */
function isGrounded(
  graph: Graph,
  nodeId: string,
  visited: Set<string>,
): boolean {
  const node = getNodeById(graph, nodeId);
  if (!node) return false;

  // Terminal bedrock: a chain that reaches here is grounded.
  if (node.type === "value") return true;

  // Cycle guard: if we're already exploring this node, treat it as not-yet
  // grounded rather than looping forever.
  if (visited.has(nodeId)) return false;
  visited.add(nodeId);

  const children = getChildren(graph, nodeId);

  let result: boolean;
  if (children.length === 0) {
    // A question with no positions, a position with no arguments, or an
    // argument that grounds in nothing — all leave a branch open.
    result = false;
  } else {
    result = children.every((child) =>
      isGrounded(graph, child.node.id, visited),
    );
  }

  // Allow this node to be re-evaluated on other paths (DAG nodes are shared).
  visited.delete(nodeId);
  return result;
}

/**
 * FULLY GROUNDED vs OPEN badge for a question node.
 */
export function isFullyGrounded(graph: Graph, questionId: string): boolean {
  return isGrounded(graph, questionId, new Set<string>());
}

/**
 * Whether a value node is reached via a "shared-value" edge from a given parent
 * argument — i.e. a value REUSED across multiple questions (the convergence
 * edge). Used to show the "↺ shared" indicator.
 */
export function isSharedValueLink(
  graph: Graph,
  parentId: string,
  valueId: string,
): boolean {
  return getEdgeType(graph, parentId, valueId) === "shared-value";
}
