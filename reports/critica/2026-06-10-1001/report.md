# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 5)`
- **Budget:** ~584k tokens (11 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 18 (5 auto, 12 diferidos, 1 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/parabola-do-festim-de-bodas.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md` | conceito | ✓ 1 auto · ⚠ 2 dif · ✕ 1 desc | 4 | 1 | 2 |
| `wiki/conceitos/penas-eternas.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/perfeicao-moral.md` | conceito | ✓ 1 auto · ⚠ 4 diferidos | 5 | 1 | 4 |
| `wiki/conceitos/perturbacao.md` | conceito | ✓ 3 auto · ⚠ 2 diferidos | 5 | 3 | 2 |

## 3. Achados por eixo

### Eixo 2 — Citações (6)

- **[media]** `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md`:17 — ✕ descartado (verificação refutou)
  - Afirmação: Blockquote (Mt 20:1-16) diverge da redação da ESE.
  - Evidência: A divergência é só entre traduções bíblicas; a página atribui o blockquote a S. Mateus, NÃO ao ESE.
  - Verificação: **refuted** — A página atribui o blockquote a S. Mateus (não ao ESE). Diferença normal entre traduções da Bíblia; sem falsa atribuição. Achado não sobrevive à verificação adversarial.
- **[media]** `wiki/conceitos/perfeicao-moral.md`:17 — ⚠ diferido a humano
  - Afirmação: Blockquote de (LE, q. 893) não-literal.
  - Evidência: Página: 'Toda virtude tem seu mérito próprio'; literal: 'Todas as virtudes têm seu mérito'. Conformar à edição Guillon/FEB.
  - Verificação: **confirmed** — cite.py: singular vs plural + 'próprio' acrescentado; está em blockquote com aspas (transcrição literal).
- **[media]** `wiki/conceitos/perfeicao-moral.md`:33 — ⚠ diferido a humano
  - Afirmação: Blockquote de (LE, q. 909) não-literal.
  - Evidência: Página: 'frequentemente, fazendo esforços muito insignificantes'; literal: 'por vezes fazendo esforços bem pequenos'.
  - Verificação: **confirmed** — cite.py: 'por vezes'→'frequentemente' inverte a frequência; 'bem pequenos'→'muito insignificantes'.
- **[baixa]** `wiki/conceitos/parabola-do-festim-de-bodas.md`:23 — ⚠ diferido a humano
  - Afirmação: Cabeçalho cita (ESE, cap. XVIII, itens 1-3).
  - Evidência: Item 1 = parábola; item 2 = toda a análise; item 3 = 'A porta estreita' (Mt 7:13-14), perícope distinta. Estreitar para 1-2.
  - Verificação: **confirmed** — cite.py: item 3 é outro logion; a citação pontual da l.31 já aponta certo (item 2). Erro só no cabeçalho.
- **[baixa]** `wiki/conceitos/perfeicao-moral.md`:43 — ⚠ diferido a humano
  - Afirmação: Blockquote de (LE, q. 917) usa 'entretenimento' onde Guillon/FEB traz 'manutenção'.
  - Evidência: cite.py: '...para cuja manutenção tudo concorre'.
  - Verificação: **confirmed** — cite.py: 'manutenção' é o termo canônico; 'entretenimento' desloca o sentido. Em blockquote citacional.
- **[baixa]** `wiki/conceitos/perturbacao.md`:19 — ⚠ diferido a humano
  - Afirmação: TOOLING — página CORRETA. cite.py não desambígua os dois 'cap. I' de C&I.
  - Evidência: Citações da página (C&I 2ª parte cap. I 'A passagem', itens 4-15) batem com ceu-e-inferno.md:2295-2318; cite.py resolve p/ 1ª parte cap. I ('O futuro e o nada'). NÃO alterar a página — corrigir o resolve_locus de cite.py.
  - Verificação: **confirmed** — Itens 4/6/8/13 conferem com 2ª parte cap. I. O 'erro' é bug de desambiguação do validador, não da wiki. Risco: futuras auditorias 'corrigirem' loci corretos.

### Eixo 3 — Padrão editorial (4)

- **[media]** `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md`:29 — ⚠ diferido a humano
  - Afirmação: 'Recompensa proporcional ao esforço individual' tensiona o item 3.
  - Evidência: ESE cap. XX item 3: os últimos podem receber recompensa MAIOR por herdarem o labor dos predecessores. Refinar o enquadramento (solidariedade/herança intelectual).
- **[baixa]** `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md`:15 — ⚠ diferido a humano
  - Afirmação: Estrutura fora do template ('Texto da parábola' extra; faltam Desdobramentos/Divergências).
  - Evidência: convencoes-frontmatter.md.
- **[baixa]** `wiki/conceitos/penas-eternas.md`:77 — ⚠ diferido a humano
  - Afirmação: Faltam 'Desdobramentos' e 'Divergências' do template.
  - Evidência: convencoes-frontmatter.md (Divergências legitimamente ausente — página é a posição de Kardec).
- **[baixa]** `wiki/conceitos/perfeicao-moral.md`:11 — ⚠ diferido a humano
  - Afirmação: Estrutura temática própria, sem 'Aplicação prática' nem 'Divergências'.
  - Evidência: convencoes-frontmatter.md.

### Eixo 4 — Tags e cross-references (8)

- **[baixa]** `wiki/conceitos/parabola-do-festim-de-bodas.md`:4 — ⚠ diferido a humano
  - Afirmação: Só tema/jesus; eixo moral da túnica nupcial é central.
  - Evidência: Avaliar tema/moral.
- **[baixa]** `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md`:4 — ✓ auto-corrigido
  - Afirmação: Só tema/jesus; bullet 3 desenvolve pluralidade das existências.
  - Evidência: Linha 31 cita (LE, q. 166-222); ESE cap. XX item 3 confirma o eixo reencarnatório.
  - Ação: `add-tag` — Adicionada tag tema/encarnacao ao frontmatter.
- **[baixa]** `wiki/conceitos/penas-eternas.md`:90 — ⚠ diferido a humano
  - Afirmação: Links anjos/demonios sem âncora na prosa.
  - Evidência: Linhas 90-91; o corpo não menciona anjos/demônios. Relação fraca via céu-e-inferno.
- **[baixa]** `wiki/conceitos/perfeicao-moral.md`:39 — ✓ auto-corrigido
  - Afirmação: 'egoísmo' tratado extensamente sem wikilink.
  - Evidência: Linha 39; existe wiki/conceitos/egoismo.md.
  - Ação: `add-wikilink` — Adicionado [[wiki/conceitos/egoismo|egoísmo]] na linha 39.
- **[baixa]** `wiki/conceitos/perturbacao.md`:60 — ✓ auto-corrigido
  - Afirmação: 'prece' em prosa sem wikilink.
  - Evidência: Linha 60; existe wiki/conceitos/prece.md.
  - Ação: `add-wikilink` — Envolveu 'prece' em [[wiki/conceitos/prece|prece]] na linha 60.
- **[baixa]** `wiki/conceitos/perturbacao.md`:60 — ✓ auto-corrigido
  - Afirmação: 'evocação' em prosa sem wikilink.
  - Evidência: Linha 60; existe wiki/conceitos/evocacao.md.
  - Ação: `add-wikilink` — Envolveu 'evocação' em [[wiki/conceitos/evocacao|evocação]] na linha 60.
- **[baixa]** `wiki/conceitos/perturbacao.md`:60 — ✓ auto-corrigido
  - Afirmação: 'passe' em prosa sem wikilink.
  - Evidência: Linha 60; existe wiki/conceitos/passe.md.
  - Ação: `add-wikilink` — Envolveu 'passe' em [[wiki/conceitos/passe|passe]] na linha 60.
- **[baixa]** `wiki/conceitos/perturbacao.md`:60 — ⚠ diferido a humano
  - Afirmação: 'desobsessão' sem wikilink (slug difere: obsessao.md).
  - Evidência: Avaliar [[wiki/conceitos/obsessao|desobsessão]] (display alternativo).

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md`:4 — `add-tag`: Adicionada tag tema/encarnacao ao frontmatter.
- `wiki/conceitos/perfeicao-moral.md`:39 — `add-wikilink`: Adicionado [[wiki/conceitos/egoismo|egoísmo]] na linha 39.
- `wiki/conceitos/perturbacao.md`:60 — `add-wikilink`: Envolveu 'prece' em [[wiki/conceitos/prece|prece]] na linha 60.
- `wiki/conceitos/perturbacao.md`:60 — `add-wikilink`: Envolveu 'evocação' em [[wiki/conceitos/evocacao|evocação]] na linha 60.
- `wiki/conceitos/perturbacao.md`:60 — `add-wikilink`: Envolveu 'passe' em [[wiki/conceitos/passe|passe]] na linha 60.

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/parabola-do-festim-de-bodas.md` (eixo 2, baixa) — Cabeçalho cita (ESE, cap. XVIII, itens 1-3).
- `wiki/conceitos/parabola-do-festim-de-bodas.md` (eixo 4, baixa) — Só tema/jesus; eixo moral da túnica nupcial é central.
- `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md` (eixo 3, media) — 'Recompensa proporcional ao esforço individual' tensiona o item 3.
- `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md` (eixo 3, baixa) — Estrutura fora do template ('Texto da parábola' extra; faltam Desdobramentos/Divergências).
- `wiki/conceitos/penas-eternas.md` (eixo 4, baixa) — Links anjos/demonios sem âncora na prosa.
- `wiki/conceitos/penas-eternas.md` (eixo 3, baixa) — Faltam 'Desdobramentos' e 'Divergências' do template.
- `wiki/conceitos/perfeicao-moral.md` (eixo 2, media) — Blockquote de (LE, q. 893) não-literal.
- `wiki/conceitos/perfeicao-moral.md` (eixo 2, media) — Blockquote de (LE, q. 909) não-literal.
- `wiki/conceitos/perfeicao-moral.md` (eixo 2, baixa) — Blockquote de (LE, q. 917) usa 'entretenimento' onde Guillon/FEB traz 'manutenção'.
- `wiki/conceitos/perfeicao-moral.md` (eixo 3, baixa) — Estrutura temática própria, sem 'Aplicação prática' nem 'Divergências'.
- `wiki/conceitos/perturbacao.md` (eixo 2, baixa) — TOOLING — página CORRETA. cite.py não desambígua os dois 'cap. I' de C&I.
- `wiki/conceitos/perturbacao.md` (eixo 4, baixa) — 'desobsessão' sem wikilink (slug difere: obsessao.md).

## 6. Resumo por página

### `wiki/conceitos/parabola-do-festim-de-bodas.md`
Fiel ao ESE cap. XVIII item 2; cabeçalho cita 'itens 1-3' mas o item 3 é 'A porta estreita' (perícope distinta); segunda tag opcional.

### `wiki/conceitos/parabola-dos-trabalhadores-da-ultima-hora.md`
Sólida; tag tema/encarnacao aplicada; blockquote DESCARTADO (é Mateus, não ESE); enquadramento mérito/recompensa tensiona item 3; estrutura.

### `wiki/conceitos/penas-eternas.md`
Fiel a C&I 1ª parte cap. VI; lint limpo; links anjos/demonios sem âncora na prosa; estrutura incompleta.

### `wiki/conceitos/perfeicao-moral.md`
Fiel; wikilink egoismo aplicado; 3 blockquotes de LE (q.893/909/917) não-literais (variantes de tradução vs Guillon/FEB); estrutura temática.

### `wiki/conceitos/perturbacao.md`
CORRETA (citações de C&I 2ª parte cap. I batem); 3 wikilinks aplicados; eixo-2 é BUG do cite.py (não desambígua os dois 'cap. I' de C&I); desobsessão opcional.
