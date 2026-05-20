/* Right rail — Quartz `right` slot.
 * Renders: Graph (mini), Table of Contents, Backlinks. */

function MiniGraph({focus = "Caridade"}) {
  /* Decorative SVG — visual recreation of the Quartz mini-graph
   * (force-directed). Not an actual force layout. */
  const center = {x: 140, y: 100};
  const sats = [
    {x: 50,  y: 50,  r: 6, label: "Amor"},
    {x: 235, y: 40,  r: 6, label: "ESE XV"},
    {x: 60,  y: 160, r: 6, label: "Egoísmo"},
    {x: 240, y: 160, r: 6, label: "Tiago"},
    {x: 150, y: 25,  r: 4, label: ""},
    {x: 30,  y: 110, r: 4, label: ""},
    {x: 260, y: 105, r: 4, label: ""},
    {x: 165, y: 175, r: 4, label: ""},
  ];
  return (
    <div className="graph-box">
      <svg viewBox="0 0 280 200" width="100%" height="100%">
        {sats.map((s, i) => (
          <line key={'l'+i} x1={center.x} y1={center.y} x2={s.x} y2={s.y}
            stroke="#b8b8b8" strokeWidth="1" opacity="0.5"/>
        ))}
        <line x1={50} y1={50} x2={60} y2={160} stroke="#b8b8b8" strokeWidth="1" opacity="0.3"/>
        <line x1={235} y1={40} x2={240} y2={160} stroke="#b8b8b8" strokeWidth="1" opacity="0.3"/>
        {sats.map((s, i) => (
          <g key={'n'+i}>
            <circle cx={s.x} cy={s.y} r={s.r} fill="#6cb55a" opacity={s.label ? 0.7 : 0.35}/>
            {s.label && (
              <text x={s.x} y={s.y + s.r + 11} textAnchor="middle"
                fontFamily="Source Sans 3" fontSize="9" fill="#4e4e4e">{s.label}</text>
            )}
          </g>
        ))}
        <circle cx={center.x} cy={center.y} r={9} fill="#4a6741"/>
        <text x={center.x} y={center.y + 22} textAnchor="middle"
          fontFamily="Schibsted Grotesk" fontSize="11" fontWeight="600" fill="#2b2b2b">{focus}</text>
      </svg>
    </div>
  );
}

function TOC({items, activeId}) {
  return (
    <nav className="toc">
      {items.map((it, i) => (
        <a key={i}
           href={`#${it.id}`}
           className={`lvl-${it.level} ${it.id === activeId ? 'active' : ''}`}>
          {it.label}
        </a>
      ))}
    </nav>
  );
}

function Backlinks({items}) {
  if (!items?.length) return (
    <div className="backlinks" style={{color:'var(--fg-3)'}}>Nenhuma página aponta para esta.</div>
  );
  return (
    <div className="backlinks">
      {items.map((b, i) => <a key={i} href="#">{b}</a>)}
    </div>
  );
}

function RightRail({focus, toc, activeTocId, backlinks}) {
  return (
    <aside className="right">
      <div className="rail-panel">
        <h6>Grafo</h6>
        <MiniGraph focus={focus}/>
      </div>
      {toc?.length > 0 && (
        <div className="rail-panel">
          <h6>Nesta página</h6>
          <TOC items={toc} activeId={activeTocId}/>
        </div>
      )}
      <div className="rail-panel">
        <h6>Backlinks</h6>
        <Backlinks items={backlinks}/>
      </div>
    </aside>
  );
}

Object.assign(window, { RightRail, MiniGraph, TOC, Backlinks });
