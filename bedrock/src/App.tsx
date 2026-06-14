import { Legend } from "./components/Legend";
import { TreeView } from "./components/TreeView";
import { ROOT_QUESTION_ID, seedGraph } from "./data/seed";

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Bedrock</h1>
        <p className="tagline">
          Drill any question down to the fundamental <em>values</em> it rests on.
          Keep clicking until each branch hits bedrock.
        </p>
      </header>

      <Legend />

      <main className="app-main">
        <TreeView graph={seedGraph} rootId={ROOT_QUESTION_ID} />
      </main>

      <footer className="app-footer">
        V1 prototype · hardcoded seed (the Trolley Problem) · browse &amp; drill only
      </footer>
    </div>
  );
}
