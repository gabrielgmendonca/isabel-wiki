/* Left rail — Quartz `left` slot.
 * Renders: PageTitle, Search, Darkmode + FontSize toolbar, Explorer tree. */

function PageTitle() {
  return (
    <div>
      <a href="#" style={{display:'block'}}>
        <div className="page-title">
          <span className="big">I</span><span className="small">s</span>
          <span className="big">A</span><span className="small">bel</span>
        </div>
      </a>
      <div className="page-title-sub">WIKI ESPÍRITA</div>
    </div>
  );
}

function SearchBox({onClick}) {
  return (
    <div className="search-box" onClick={onClick}>
      <Icons.Search/>
      <span>Buscar…</span>
      <kbd>Ctrl K</kbd>
    </div>
  );
}

function Toolbar({dark, setDark, fontScale, setFontScale}) {
  return (
    <div className="toolbar">
      <button
        className="icon-btn"
        title={dark ? "Modo claro" : "Modo escuro"}
        onClick={()=>setDark(!dark)}>
        {dark ? <Icons.Sun/> : <Icons.Moon/>}
      </button>
      <div className="fontsize-toggle">
        <span className="lbl">Aa</span>
        <button onClick={()=>setFontScale(Math.max(-2, fontScale-1))} style={{fontSize:12}} title="Diminuir">A−</button>
        <button onClick={()=>setFontScale(Math.min(2, fontScale+1))} style={{fontSize:14}} title="Aumentar">A+</button>
      </div>
    </div>
  );
}

/* Explorer — collapsible tree. */
function TreeNode({node, depth=0, currentPath, onNavigate}) {
  const [open, setOpen] = React.useState(node.openByDefault ?? depth < 1);
  const isLeaf = !node.children?.length;
  const isCurrent = currentPath === node.path;
  return (
    <div>
      <div
        className={`tree-row ${open ? 'open' : ''} ${isCurrent ? 'current' : ''}`}
        onClick={() => isLeaf ? onNavigate?.(node) : setOpen(!open)}>
        {isLeaf ? <span className="leaf"/> : <Icons.Chevron size={10}/>}
        <span>{node.label}</span>
      </div>
      {open && node.children && (
        <div className="tree-children">
          {node.children.map((c, i) => (
            <TreeNode key={i} node={c} depth={depth+1} currentPath={currentPath} onNavigate={onNavigate}/>
          ))}
        </div>
      )}
    </div>
  );
}

function Explorer({tree, currentPath, onNavigate}) {
  const [open, setOpen] = React.useState(true);
  return (
    <div className="explorer">
      <div className="explorer-title" onClick={() => setOpen(!open)}>
        <Icons.ChevronDn size={10} style={{transform: open ? 'none' : 'rotate(-90deg)'}}/>
        Explorer
      </div>
      {open && (
        <div className="explorer-tree">
          {tree.map((n, i) => (
            <TreeNode key={i} node={n} currentPath={currentPath} onNavigate={onNavigate}/>
          ))}
        </div>
      )}
    </div>
  );
}

function LeftRail({tree, currentPath, onNavigate, dark, setDark, fontScale, setFontScale, onSearch}) {
  return (
    <aside className="left">
      <PageTitle/>
      <SearchBox onClick={onSearch}/>
      <Toolbar dark={dark} setDark={setDark} fontScale={fontScale} setFontScale={setFontScale}/>
      <Explorer tree={tree} currentPath={currentPath} onNavigate={onNavigate}/>
    </aside>
  );
}

Object.assign(window, { LeftRail, PageTitle, SearchBox, Toolbar, Explorer, TreeNode });
