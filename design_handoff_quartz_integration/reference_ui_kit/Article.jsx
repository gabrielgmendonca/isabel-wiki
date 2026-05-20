/* Article components — Breadcrumbs, ArticleTitle/Meta/Tags, Callout, AffordanceCard. */

function Breadcrumbs({path}) {
  return (
    <div className="crumbs">
      {path.map((p, i) => {
        const last = i === path.length - 1;
        return (
          <React.Fragment key={i}>
            {last
              ? <span className="curr">{p.label}</span>
              : <a href="#">{p.label}</a>}
            {!last && <span className="sep">›</span>}
          </React.Fragment>
        );
      })}
    </div>
  );
}

function ArticleHead({title, meta, tags}) {
  return (
    <>
      <h1 className="article-title">{title}</h1>
      <div className="article-meta">
        {meta.map((m, i) => (
          <React.Fragment key={i}>
            <span>{m}</span>
            {i < meta.length-1 && <span style={{color:'var(--lightgray)'}}>·</span>}
          </React.Fragment>
        ))}
      </div>
      <div className="taglist">
        {tags.map((t, i) => <span className="tag-chip" key={i}>{t}</span>)}
      </div>
    </>
  );
}

function Callout({kind = "note", title, children}) {
  const icon = kind === "warning" ? <Icons.Warning/> : kind === "tip" ? <Icons.Bulb/> : null;
  return (
    <div className={`callout ${kind}`}>
      {title && (
        <div className="callout-title">{icon}{title}</div>
      )}
      <div>{children}</div>
    </div>
  );
}

function AffordanceCard({icon, title, desc, center}) {
  return (
    <div className={`affordance ${center ? 'center' : ''}`}>
      <div className="head">{icon}<a href="#">{title}</a></div>
      <div className="desc">{desc}</div>
    </div>
  );
}

function WikiLink({term, children}) {
  return <a href="#" title={`[[wiki/conceitos/${term}]]`}>{children || term}</a>;
}

function Glossary({term, children}) {
  return <abbr title={term}>{children}</abbr>;
}

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-cc">
        <a href="#"><img src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png" alt="CC BY-NC-SA 4.0" width="88" height="31"/></a>
        <span>Conteúdo licenciado sob <a href="#">CC BY-NC-SA 4.0</a></span>
      </div>
      <p>Feito com <a href="https://quartz.jzhao.xyz/">Quartz v4.4.0</a> © 2026</p>
      <ul>
        <li><a href="https://github.com/gabrielgmendonca/isabel-wiki">GitHub</a></li>
        <li><a href="#">Sugerir correção</a></li>
      </ul>
    </footer>
  );
}

Object.assign(window, { Breadcrumbs, ArticleHead, Callout, AffordanceCard, WikiLink, Glossary, Footer });
