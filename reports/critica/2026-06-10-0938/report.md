# Relatório de crítica profunda — 2026-06-10

## 1. Metadados do run

- **Data:** 2026-06-10
- **Escopo:** `--limit 5 (loop, lote 3)`
- **Budget:** ~574k tokens (10 agentes)
- **Modelos:** critica=opus, verificacao=sonnet
- **Páginas devidas / criticadas / puladas:** 5 / 5 / 0
- **Total de achados:** 10 (1 auto, 9 diferidos, 0 descartados)

## 2. Páginas avaliadas

| Página | Tipo | Veredito | Achados | Auto | Diferidos |
|--------|------|----------|---------|------|-----------|
| `wiki/conceitos/erraticidade.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/evocacao.md` | conceito | ✓ 1 auto · ⚠ 2 diferidos | 3 | 1 | 2 |
| `wiki/conceitos/futuro-e-o-nada.md` | conceito | ✓ limpa · ⚠ 1 cross-ref | 1 | 0 | 1 |
| `wiki/conceitos/homem-de-bem.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |
| `wiki/conceitos/ligacao-espirito-corpo.md` | conceito | ⚠ 2 diferidos | 2 | 0 | 2 |

## 3. Achados por eixo

### Eixo 2 — Citações (5)

- **[alta]** `wiki/conceitos/homem-de-bem.md`:33 — ⚠ diferido a humano
  - Afirmação: Apresenta como literal de (LE, q. 893): 'A perfeição moral consiste em praticar a lei de justiça, de amor e de caridade, na sua maior pureza'.
  - Evidência: q. 893 trata da virtude mais meritória (caridade desinteressada). A fórmula é do comentário à q. 918 ('O verdadeiro homem de bem é o que pratica a lei de justiça, amor e caridade, na sua maior pureza'). A frase 'A perfeição moral consiste em...' não é verbatim em lugar nenhum.
  - Verificação: **confirmed** — cite.py: q. 893 ≠ fórmula citada; a fórmula é da q. 918. Conflação do título do cap. XII com a q. 918. Misatribuição de locus.
- **[alta]** `wiki/conceitos/ligacao-espirito-corpo.md`:29 — ⚠ diferido a humano
  - Afirmação: Rompimento do laço perispiritual 'é gradual na morte natural e pode ser mais abrupto na morte violenta' (LE, q. 155-162).
  - Evidência: q. 162 (nota): na morte violenta 'mais tenazes são os laços... mais lento o desprendimento completo'; q. 165: a ilusão se prolonga. A página INVERTE Kardec — na morte violenta o desligamento é mais LENTO, não mais abrupto.
  - Verificação: **confirmed** — cite.py: q. 162 nota + q. 165 dizem o oposto da página. Sentido invertido — o abrupto é a cessação da vida orgânica/perturbação, não o rompimento do laço.
- **[media]** `wiki/conceitos/erraticidade.md`:29 — ⚠ diferido a humano
  - Afirmação: 'Auxiliar os encarnados como Espírito protetor ou guia' atribuído a (LE, q. 229).
  - Evidência: q. 229 trata da retenção das más paixões após a morte. Suporte real: q. 226 (missões/ocupações ativas) e o capítulo dos Espíritos protetores (q. 489 ss.).
  - Verificação: **confirmed** — cite.py: q. 229 fala da persistência dos vícios, não de proteção aos encarnados. Locus errado.
- **[media]** `wiki/conceitos/evocacao.md`:37 — ⚠ diferido a humano
  - Afirmação: 'Qualquer Espírito, de qualquer época' acode, com frase entre aspas atribuída a (LM, item 272).
  - Evidência: Item 272 trata da dificuldade das evocações; a frase não é literal. Item 282 (2ª-3ª) condiciona e lista Espíritos que NUNCA podem comunicar-se (mundos inferiores à Terra; esferas de punição).
  - Verificação: **confirmed** — cite.py: item 272 não afirma que qualquer Espírito acode; item 282 contradiz o enquadramento universal. Locus errado + afirmação forte demais.
- **[media]** `wiki/conceitos/ligacao-espirito-corpo.md`:25 — ⚠ diferido a humano
  - Afirmação: Desprendimento parcial em sono/êxtase/sonambulismo citado com '(LE, q. 400-455; LM, 2ª parte, cap. VI)'.
  - Evidência: LM 2ª parte cap. VI é 'Das manifestações visuais' (aparições), não emancipação da alma; o próprio cap. remete a LE 'Da emancipação da alma' q. 409. Locus correto: LE q. 400-455.
  - Verificação: **confirmed** — cite.py + leitura do LM: cap. VI trata de aparições; a nota do próprio capítulo redireciona ao LE q. 409. Remover (LM, 2ª parte, cap. VI) da linha 25 e das Fontes.

### Eixo 3 — Padrão editorial (3)

- **[media]** `wiki/conceitos/homem-de-bem.md`:21 — ⚠ diferido a humano
  - Afirmação: Paráfrases de (ESE, cap. XVII, item 3) apresentadas entre aspas como literais (linhas 21, 25, 27, 29).
  - Evidência: Locus correto e conteúdo fiel em substância; mas as frases entre aspas não são verbatim. A quote da linha 23 ('Retribui o mal com o bem...') é verbatim e pode ficar.
- **[baixa]** `wiki/conceitos/erraticidade.md`:37 — ⚠ diferido a humano
  - Afirmação: Faltam seções 'Desdobramentos' e 'Divergências' do template de conceito.
  - Evidência: convencoes-frontmatter.md.
- **[baixa]** `wiki/conceitos/evocacao.md`:51 — ⚠ diferido a humano
  - Afirmação: Faltam seções 'Desdobramentos' e 'Divergências' do template de conceito.
  - Evidência: convencoes-frontmatter.md (opcionais sem conteúdo).

### Eixo 4 — Tags e cross-references (2)

- **[baixa]** `wiki/conceitos/evocacao.md`:53 — ✓ auto-corrigido
  - Afirmação: 'prece' sem wikilink (página existe).
  - Evidência: Linha 53; alvo wiki/conceitos/prece.md existe.
  - Ação: `add-wikilink` — Envolveu 'prece' (ocorrência isolada, linha 53) em [[wiki/conceitos/prece|prece]].
- **[baixa]** `wiki/conceitos/futuro-e-o-nada.md`:47 — ⚠ diferido a humano
  - Afirmação: Cross-ref opcional a [[wiki/conceitos/materialismo]] ausente.
  - Evidência: Linha 47 fala em 'combate ao materialismo contemporâneo'; página materialismo.md existe. Adversário central do argumento de C&I cap. I.

## 4. Mudanças auto-aplicadas

- `wiki/conceitos/evocacao.md`:53 — `add-wikilink`: Envolveu 'prece' (ocorrência isolada, linha 53) em [[wiki/conceitos/prece|prece]].

## 5. Diferidos a decisão humana

> Páginas marcadas `status: rascunho`; itens anotados no ROADMAP.md §11.

- `wiki/conceitos/erraticidade.md` (eixo 2, media) — 'Auxiliar os encarnados como Espírito protetor ou guia' atribuído a (LE, q. 229).
- `wiki/conceitos/erraticidade.md` (eixo 3, baixa) — Faltam seções 'Desdobramentos' e 'Divergências' do template de conceito.
- `wiki/conceitos/evocacao.md` (eixo 2, media) — 'Qualquer Espírito, de qualquer época' acode, com frase entre aspas atribuída a (LM, item 272).
- `wiki/conceitos/evocacao.md` (eixo 3, baixa) — Faltam seções 'Desdobramentos' e 'Divergências' do template de conceito.
- `wiki/conceitos/futuro-e-o-nada.md` (eixo 4, baixa) — Cross-ref opcional a [[wiki/conceitos/materialismo]] ausente.
- `wiki/conceitos/homem-de-bem.md` (eixo 2, alta) — Apresenta como literal de (LE, q. 893): 'A perfeição moral consiste em praticar a lei de justiça, de amor e de caridade, na sua maior pureza'.
- `wiki/conceitos/homem-de-bem.md` (eixo 3, media) — Paráfrases de (ESE, cap. XVII, item 3) apresentadas entre aspas como literais (linhas 21, 25, 27, 29).
- `wiki/conceitos/ligacao-espirito-corpo.md` (eixo 2, alta) — Rompimento do laço perispiritual 'é gradual na morte natural e pode ser mais abrupto na morte violenta' (LE, q. 155-162).
- `wiki/conceitos/ligacao-espirito-corpo.md` (eixo 2, media) — Desprendimento parcial em sono/êxtase/sonambulismo citado com '(LE, q. 400-455; LM, 2ª parte, cap. VI)'.

## 6. Resumo por página

### `wiki/conceitos/erraticidade.md`
Fiel ao LE cap. VI; locus q. 229 errado para 'protetor/guia' (real: q. 226 / q. 489 ss.); estrutura incompleta.

### `wiki/conceitos/evocacao.md`
Sólida; wikilink prece adicionado; 'qualquer Espírito acode' (item 272) forte demais — item 282 condiciona; estrutura incompleta.

### `wiki/conceitos/futuro-e-o-nada.md`
Estudo fiel de C&I 1ª parte cap. I — 13 citações conferem; lint limpo; único ponto é cross-ref opcional a materialismo.

### `wiki/conceitos/homem-de-bem.md`
Retrato fiel (ESE cap. XVII item 3 é o locus certo); fórmula atribuída a q. 893 é da q. 918; paráfrases de ESE item 3 entre aspas como literais.

### `wiki/conceitos/ligacao-espirito-corpo.md`
Núcleo sólido, mas afirma rompimento 'mais abrupto na morte violenta' invertendo Kardec; e cita LM 2ª parte cap. VI (manifestações visuais) para emancipação da alma (locus real: LE q. 400-455).
