// A small, static legend explaining the four node types and their colours.
const ITEMS: { variant: string; marker: string; label: string; blurb: string }[] = [
  { variant: "question", marker: "?", label: "Question", blurb: "Something to drill into." },
  { variant: "position", marker: "▸", label: "Position", blurb: "A candidate answer." },
  {
    variant: "argument-support",
    marker: "✓",
    label: "Argument · supports",
    blurb: "A reason backing a position.",
  },
  {
    variant: "argument-attack",
    marker: "✕",
    label: "Argument · attacks",
    blurb: "A reason undermining a position.",
  },
  {
    variant: "value",
    marker: "⚓",
    label: "Bedrock value",
    blurb: "Terminal — a chain bottoms out here.",
  },
];

export function Legend() {
  return (
    <aside className="legend" aria-label="Legend">
      {ITEMS.map((item) => (
        <div key={item.variant} className="legend-item">
          <span className={`legend-swatch card-${item.variant}`} aria-hidden="true">
            {item.marker}
          </span>
          <div className="legend-text">
            <strong>{item.label}</strong>
            <span>{item.blurb}</span>
          </div>
        </div>
      ))}
      <div className="legend-item legend-badges">
        <span className="badge badge-grounded">FULLY GROUNDED</span>
        <span className="badge badge-open">OPEN</span>
        <span className="badge badge-shared">↺ shared</span>
      </div>
    </aside>
  );
}
