/* Screens — Home, ArticleCaridade. */

const TREE = [
  { label: "wiki", openByDefault: true, path: "wiki", children: [
    { label: "conceitos", openByDefault: true, path: "wiki/conceitos", children: [
      { label: "arrependimento", path: "wiki/conceitos/arrependimento" },
      { label: "caridade",       path: "wiki/conceitos/caridade" },
      { label: "expiação",        path: "wiki/conceitos/expiacao" },
      { label: "fé",              path: "wiki/conceitos/fe" },
      { label: "livre-arbítrio",  path: "wiki/conceitos/livre-arbitrio" },
      { label: "reencarnação",    path: "wiki/conceitos/reencarnacao" },
    ]},
    { label: "obras", path: "wiki/obras", children: [
      { label: "livro-dos-espiritos",         path: "wiki/obras/livro-dos-espiritos" },
      { label: "evangelho-segundo-o-espiritismo", path: "wiki/obras/evangelho-segundo-o-espiritismo" },
      { label: "a-genese",                    path: "wiki/obras/a-genese" },
    ]},
    { label: "sínteses", path: "wiki/sinteses", children: [
      { label: "catalogo",                 path: "wiki/sinteses/catalogo" },
      { label: "glossario",                path: "wiki/sinteses/glossario" },
      { label: "hierarquia-de-autoridade", path: "wiki/sinteses/hierarquia-de-autoridade" },
    ]},
    { label: "trilhas", path: "wiki/trilhas", children: [
      { label: "primeiros-passos", path: "wiki/trilhas/primeiros-passos" },
      { label: "esde",             path: "wiki/trilhas/esde" },
      { label: "palestras",        path: "wiki/trilhas/palestras" },
    ]},
    { label: "personalidades", path: "wiki/personalidades", children: [] },
    { label: "questões",        path: "wiki/questoes",      children: [] },
    { label: "divergências",    path: "wiki/divergencias",  children: [] },
    { label: "aprofundamentos", path: "wiki/aprofundamentos", children: [] },
  ]},
];

/* ── Home screen — recreates index.md ─────────────────────────────── */
function Home() {
  return (
    <article className="article" data-screen-label="Home">
      <h1 className="article-title" style={{textAlign:'center', marginBottom: 8}}>
        Bem-vindo à IsAbel
      </h1>
      <p style={{textAlign:'center', fontSize:17, color:'var(--darkgray)', marginBottom: 32}}>
        <strong>IsAbel</strong> é uma wiki de estudo da Doutrina Espírita codificada por
        Allan Kardec. Criada como ferramenta pessoal de estudo e preparação de palestras
        em casas espíritas, aberta a qualquer estudante sério que queira consultar.
      </p>

      <div className="prose">
        <h2>Para que você veio?</h2>
        <div className="affordances">
          <AffordanceCard icon={<Icons.Book/>}  title="Estou chegando agora"      desc="Introdução ao Espiritismo em passos guiados."/>
          <AffordanceCard icon={<Icons.Cap/>}   title="Preparo estudos doutrinários" desc="Trilhas para ESDE e evangelização infantojuvenil."/>
          <AffordanceCard icon={<Icons.Mic/>}   title="Preparo uma palestra"        desc="Parábolas, sínteses e slides prontos."/>
          <AffordanceCard icon={<Icons.Books/>} title="Quero ler livremente"        desc="Pentateuco e obras complementares em ordem."/>
        </div>
        <AffordanceCard center icon={<Icons.Lens/>} title="Consulta rápida" desc="Glossário de termos espíritas + busca no topo."/>

        <h2>Hierarquia de autoridade</h2>
        <p>A wiki segue uma hierarquia clara de fontes:</p>
        <ol>
          <li><strong>Ensinamentos morais de Jesus</strong> (Evangelhos canônicos) — fonte primordial.</li>
          <li><strong>Pentateuco de Kardec</strong> — LE, LM, ESE, C&amp;I, Gênese. Base inamovível.</li>
          <li><strong>Kardec complementar</strong> — OQE, OPE, <em>Revista Espírita</em>.</li>
          <li><strong>Complementares consagrados</strong> — Chico Xavier, Léon Denis, Divaldo, Emmanuel, André Luiz.</li>
          <li><strong>Complementares secundários</strong> — alinhados à codificação, sem o peso doutrinário do nível 3.</li>
        </ol>
        <p>Quando complementares contradizem o Pentateuco, <strong>Kardec prevalece</strong>. Divergências são registradas, nunca apagadas.</p>

        <h2>Status</h2>
        <Callout kind="warning" title="Trabalho em andamento">
          Esta wiki é um projeto vivo. Há páginas em rascunho, lacunas de cobertura e
          temas ainda não abordados. Toda contribuição passa por revisão humana.
        </Callout>
        <p><strong>Cobertura atual:</strong> Pentateuco completo (5/5 obras ingeridas) + Evangelhos canônicos + 108 fontes complementares. ~568 páginas entre conceitos, obras, personalidades, questões, aprofundamentos e sínteses.</p>
        <Callout kind="tip" title="Navegação avançada">
          Use a <strong>barra de busca</strong> no topo para encontrar qualquer tema.
          O <strong>explorer</strong> (barra lateral) mostra a árvore completa.
          O <strong>grafo interativo</strong> revela as conexões.
        </Callout>
      </div>
    </article>
  );
}

/* ── Article screen — Caridade (wiki/conceitos/caridade.md) ───────── */
function ArticleCaridade() {
  return (
    <article className="article" data-screen-label="Caridade">
      <Breadcrumbs path={[
        { label: "Início" }, { label: "wiki" }, { label: "conceitos" }, { label: "Caridade" }
      ]}/>
      <ArticleHead
        title="Caridade"
        meta={["tipo: conceito", "fontes: ESE, LE", "atualizado em 2026-04-27"]}
        tags={["caridade","amor","egoismo","beneficencia","moral","tiago","obra/ese","obra/le","lei/justica-amor-caridade","autor/kardec","grau/intermediario","tema/moral"]}
      />

      <div className="prose">
        <h2 id="definicao">Definição</h2>
        <p>Virtude suprema que resume toda a lei moral: amor ao próximo em pensamentos, palavras e ações. Compreende tanto a beneficência material quanto a indulgência, o perdão e a benevolência — a caridade moral.</p>

        <h2 id="ensino">Ensino de Kardec</h2>
        <h3 id="fora-da-caridade">"Fora da caridade não há salvação"</h3>
        <p>
          Máxima central do <WikiLink term="evangelho-segundo-o-espiritismo">ESE</WikiLink>, cap. XV:
          "Fora da caridade não há salvação" — entendida não como exclusivismo de seita,
          mas como lei universal. "Cada um será julgado segundo as suas obras"
          (ESE, cap. XV, item 10). Não importa a crença professada de lábios, mas a
          prática efetiva do bem.
        </p>

        <h3 id="material-moral">Caridade material e caridade moral</h3>
        <p>Kardec distingue duas faces complementares da caridade:</p>
        <ul>
          <li><strong>Caridade material</strong> (beneficência): dar o pão, o abrigo, o socorro ao necessitado. "Dar ao pobre é restituir-lhe o que lhe é devido" (ESE, cap. XIII, item 6).</li>
          <li><strong>Caridade moral</strong>: a indulgência para com o próximo, o perdão das ofensas, a benevolência em todas as relações.</li>
        </ul>

        <h3 id="paulo">A caridade segundo S. Paulo</h3>
        <p>
          S. Paulo sintetiza a caridade em termos imortais. Kardec comenta que sem a
          caridade de nada valem a eloquência, a ciência ou mesmo a <Glossary term="Fé — convicção íntima, raciocinada; ver wiki/conceitos/fe">fé</Glossary>.
        </p>
        <blockquote>
          <p>"A caridade é paciente, é benigna; a caridade não é invejosa, não é temerária, não se ensoberbece; tudo desculpa, tudo crê, tudo espera, tudo suporta."</p>
          <p style={{fontStyle:'normal', fontSize:13, color:'var(--fg-3)', marginTop: 8}}>
            <strong>1 Coríntios, 13:4–7</strong> · cit. <strong>ESE, cap. XV, item 4</strong>
          </p>
        </blockquote>

        <h4 id="filo">Nota filológica: "amor" ou "caridade"?</h4>
        <p>
          A Bíblia ACF traduz a palavra grega <em>agape</em> como <strong>"amor"</strong>.
          Kardec, seguindo a Vulgata latina (<code>caritas</code>) e a tradução francesa
          de Louis Segond, cita a mesma passagem como <strong>"caridade"</strong>.
        </p>

        <Callout kind="tip" title="Ver também">
          <WikiLink term="leis-morais/lei-de-justica-amor-e-caridade">Lei de justiça, amor e caridade</WikiLink>{' '}
          · <WikiLink term="homem-de-bem">homem de bem</WikiLink>
          {' '}· <WikiLink term="parabola-do-bom-samaritano">parábola do bom samaritano</WikiLink>
        </Callout>

        <h2 id="fontes">Fontes</h2>
        <ul>
          <li>Kardec, Allan. <em>O Evangelho Segundo o Espiritismo</em>. Trad. Guillon Ribeiro. Rio de Janeiro: FEB. Caps. XI, XIII, XV.</li>
          <li>Kardec, Allan. <em>O Livro dos Espíritos</em>. Trad. Guillon Ribeiro. Rio de Janeiro: FEB. Parte 3, cap. XI (q. 886–892).</li>
        </ul>
      </div>
    </article>
  );
}

Object.assign(window, { TREE, Home, ArticleCaridade });
