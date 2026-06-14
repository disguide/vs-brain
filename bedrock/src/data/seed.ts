import type { Graph } from "./types";

// ---------------------------------------------------------------------------
// SEED DATA — The Trolley Problem.
//
// This is the whole point of the app rendered as data: a question that, pushed
// deep enough, does not have one universal answer. It resolves into a FORK
// between two bedrock values:
//
//   "Minimize total suffering"  vs  "Never use a person merely as a means"
//
// HOW TO READ THE EDGES
// Edges are authored in their natural *semantic* direction (the same direction
// they will have as rows in Supabase later), which is NOT always top-to-bottom
// in the tree:
//   answers      : position  -> question   (a position answers a question)
//   supports     : argument  -> position   (an argument backs a position)
//   attacks      : argument  -> position   (an argument undermines a position)
//   raises       : argument  -> question   (an argument raises a sub-question)
//   grounds-in   : argument  -> value      (an argument bottoms out at a value)
//   shared-value : argument  -> value      (grounds-in for a REUSED value)
//
// The tree view in lib/graph.ts knows how to orient each edge type so the
// drill-down still reads question -> position -> argument -> (sub-question | value).
//
// TO ADD CONTENT: edit only this file. See README.md for a worked example.
// ---------------------------------------------------------------------------

export const seedGraph: Graph = {
  nodes: [
    // ----- Root question -----
    {
      id: "q-root",
      type: "question",
      content:
        "Should you pull the lever to divert the trolley, killing 1 person to save 5?",
    },

    // ----- Position A: pull the lever -----
    { id: "pos-a", type: "position", content: "Yes, pull the lever" },
    {
      id: "arg-a1",
      type: "argument",
      stance: "support",
      content: "It results in fewer deaths — 1 instead of 5",
    },
    {
      id: "q-consequences",
      type: "question",
      content: "Is the right action the one that produces the best outcome?",
    },
    {
      id: "pos-consequences",
      type: "position",
      content: "Yes, consequences determine rightness",
    },
    {
      id: "arg-consequences",
      type: "argument",
      stance: "support",
      content:
        "What matters morally is how much harm or wellbeing results",
    },
    {
      id: "val-suffering",
      type: "value",
      isTerminal: true,
      content: "Minimize total suffering",
    },

    // ----- Position B: do not pull the lever -----
    { id: "pos-b", type: "position", content: "No, do not pull the lever" },
    {
      id: "arg-b1",
      type: "argument",
      stance: "support",
      content:
        "Pulling makes you actively kill someone who would otherwise live",
    },
    {
      id: "q-killing",
      type: "question",
      content: "Is there a moral difference between killing and letting die?",
    },
    {
      id: "pos-killing",
      type: "position",
      content: "Yes, actively killing is worse than allowing a death",
    },
    {
      id: "arg-killing",
      type: "argument",
      stance: "support",
      content:
        "Using one person's death as a means to save others treats them as a tool",
    },
    {
      id: "val-means",
      type: "value",
      isTerminal: true,
      content: "Never use a person merely as a means",
    },
  ],

  edges: [
    // --- Position A branch ---
    { id: "e1", from: "pos-a", to: "q-root", edgeType: "answers" },
    { id: "e2", from: "arg-a1", to: "pos-a", edgeType: "supports" },
    { id: "e3", from: "arg-a1", to: "q-consequences", edgeType: "raises" },
    {
      id: "e4",
      from: "pos-consequences",
      to: "q-consequences",
      edgeType: "answers",
    },
    {
      id: "e5",
      from: "arg-consequences",
      to: "pos-consequences",
      edgeType: "supports",
    },
    {
      id: "e6",
      from: "arg-consequences",
      to: "val-suffering",
      edgeType: "grounds-in",
    },

    // --- Position B branch ---
    { id: "e7", from: "pos-b", to: "q-root", edgeType: "answers" },
    { id: "e8", from: "arg-b1", to: "pos-b", edgeType: "supports" },
    { id: "e9", from: "arg-b1", to: "q-killing", edgeType: "raises" },
    { id: "e10", from: "pos-killing", to: "q-killing", edgeType: "answers" },
    { id: "e11", from: "arg-killing", to: "pos-killing", edgeType: "supports" },
    { id: "e12", from: "arg-killing", to: "val-means", edgeType: "grounds-in" },
  ],
};

// The node the app opens on.
export const ROOT_QUESTION_ID = "q-root";
