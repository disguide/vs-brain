// The core data model for Bedrock.
//
// The graph is a DAG (directed acyclic graph): a node CAN have multiple parents.
// Value nodes especially are shared across many questions, so never assume a
// strict tree when traversing.

export type NodeType = "question" | "position" | "argument" | "value";

export type Stance = "support" | "attack";

export type EdgeType =
  | "answers" // position  -> question : this position answers this question
  | "supports" // argument  -> position : argument backs the position
  | "attacks" // argument  -> position : argument undermines the position
  | "raises" // argument  -> question : this argument raises a new sub-question
  | "grounds-in" // argument  -> value    : this argument bottoms out at this value (terminal)
  | "shared-value"; // argument -> value   : grounds-in for a value REUSED across questions

export interface GraphNode {
  id: string;
  type: NodeType;
  content: string;
  stance?: Stance; // only for arguments
  isTerminal?: boolean; // true for values
}

export interface GraphEdge {
  id: string;
  from: string; // node id
  to: string; // node id
  edgeType: EdgeType;
}

export interface Graph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}
