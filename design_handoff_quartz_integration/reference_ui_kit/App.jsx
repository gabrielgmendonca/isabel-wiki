/* App shell — routes between Home and ArticleCaridade. */
const { useState, useEffect } = React;

function App() {
  const [route, setRoute] = useState("home");  // 'home' | 'caridade'
  const [dark, setDark] = useState(false);
  const [fontScale, setFontScale] = useState(0);  // -2..2

  useEffect(() => {
    document.documentElement.style.setProperty('font-size', `${16 + fontScale * 1}px`);
  }, [fontScale]);

  useEffect(() => {
    if (dark) document.documentElement.setAttribute('saved-theme', 'dark');
    else document.documentElement.removeAttribute('saved-theme');
  }, [dark]);

  const onNavigate = (node) => {
    if (node.path === 'wiki/conceitos/caridade') setRoute('caridade');
    else setRoute('home');
  };

  const currentPath = route === 'caridade' ? 'wiki/conceitos/caridade' : '';

  const caridadeToc = [
    { id: 'definicao',      label: 'Definição',                 level: 2 },
    { id: 'ensino',         label: 'Ensino de Kardec',          level: 2 },
    { id: 'fora-da-caridade', label: '"Fora da caridade…"',     level: 3 },
    { id: 'material-moral', label: 'Caridade material e moral', level: 3 },
    { id: 'paulo',          label: 'S. Paulo',                  level: 3 },
    { id: 'filo',           label: 'Nota filológica',           level: 3 },
    { id: 'fontes',         label: 'Fontes',                    level: 2 },
  ];

  return (
    <>
      <div className="page" data-screen-label={route === 'home' ? '01 Home' : '02 Artigo · Caridade'}>
        <LeftRail
          tree={TREE}
          currentPath={currentPath}
          onNavigate={onNavigate}
          dark={dark} setDark={setDark}
          fontScale={fontScale} setFontScale={setFontScale}
          onSearch={() => alert('Buscar — protótipo')}
        />
        {route === 'home'
          ? <Home/>
          : <ArticleCaridade/>}
        <RightRail
          focus={route === 'home' ? 'IsAbel' : 'Caridade'}
          toc={route === 'caridade' ? caridadeToc : []}
          activeTocId="paulo"
          backlinks={route === 'caridade'
            ? ['homem-de-bem','egoísmo','lei-de-justica-amor-e-caridade','parábola-do-bom-samaritano']
            : []}
        />
      </div>
      <Footer/>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App/>);
