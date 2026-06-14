import { useState } from "react";
import type { EdgeType, Graph } from "../data/types";
import { getChildren } from "../lib/graph";
import { NodeCard } from "./NodeCard";

interface TreeNodeProps {
  graph: Graph;
  nodeId: string;
  viaEdge?: EdgeType;
  depth: number;
  /** Node ids on the path from the root to this node — used to break cycles. */
  ancestors: string[];
}

/**
 * One node in the drill-down, with its (lazily revealed) children indented
 * beneath it. Expand/collapse state lives here, so each rendered instance keeps
 * its own state — important because a shared node (a value) can appear under
 * several parents in this DAG.
 */
function TreeNode({ graph, nodeId, viaEdge, depth, ancestors }: TreeNodeProps) {
  // Root question starts open so the fork is visible on load; deeper nodes
  // start collapsed so the user drills down deliberately.
  const [expanded, setExpanded] = useState(depth === 0);

  const node = graph.nodes.find((n) => n.id === nodeId);
  if (!node) return null;

  // Cycle guard: never render a node that is already one of our ancestors.
  const children = ancestors.includes(nodeId) ? [] : getChildren(graph, nodeId);

  return (
    <div className="tree-node" style={{ marginLeft: depth === 0 ? 0 : "1.25rem" }}>
      <NodeCard
        graph={graph}
        node={node}
        viaEdge={viaEdge}
        expanded={expanded}
        onToggle={() => setExpanded((e) => !e)}
      />

      {expanded && children.length > 0 && (
        <div className="tree-children">
          {children.map((child) => (
            <TreeNode
              key={`${nodeId}->${child.node.id}`}
              graph={graph}
              nodeId={child.node.id}
              viaEdge={child.edgeType}
              depth={depth + 1}
              ancestors={[...ancestors, nodeId]}
            />
          ))}
        </div>
      )}
    </div>
  );
}

interface TreeViewProps {
  graph: Graph;
  rootId: string;
}

/** The recursive drill-down tree, rooted at `rootId`. */
export function TreeView({ graph, rootId }: TreeViewProps) {
  return (
    <div className="tree-view">
      <TreeNode graph={graph} nodeId={rootId} depth={0} ancestors={[]} />
    </div>
  );
}
