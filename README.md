# isabel-wiki

**IsAbel** é uma wiki de estudo da Doutrina Espírita codificada por Allan
Kardec — base de conhecimento mantida com GenAI (Claude Code) sob curadoria
humana, publicada via Quartz no GitHub Pages.

🌐 **Site publicado:** <https://gabrielgmendonca.github.io/isabel-wiki>

## Propósito

Ferramenta pessoal de estudo e preparação de palestras em casas espíritas,
aberta a qualquer estudante sério que queira consultar. O princípio que orienta
o crescimento da base: **cada dúvida doutrinária é oportunidade de capitalizar
conhecimento** — transformar uma resposta efêmera em página citável e fundada em
fonte. A wiki não acumula opinião; acumula doutrina referenciada.

Tom: estudante kardecista sério — respeitoso, fraterno, didático. Sem ironia,
relativismo acadêmico distanciado ou devocionalismo excessivo.

## Como o conhecimento é organizado

Toda afirmação doutrinária leva citação, e as fontes obedecem a uma hierarquia
de autoridade explícita:

- **Primordial** — ensinamentos morais de Jesus (Evangelhos canônicos).
- **1 — Pentateuco de Kardec** (LE, LM, ESE, C&I, Gênese): base inamovível.
- **2 — Kardec complementar** (OQE, OPE, *Revista Espírita*…).
- **3 — Consagrados** (Chico Xavier, Léon Denis, Divaldo, Emmanuel, André Luiz…).
- **4 — Secundários** — alinhados à codificação, sem o peso do nível 3.

Quando um nível inferior contradiz o Pentateuco, **Kardec prevalece** — e a
divergência é registrada, nunca apagada.

## Como é construída

Mantida via Claude Code com skills versionadas que padronizam o trabalho:
`/ingest` (ingerir uma fonte), `/lint` (integridade e consistência), `/slides`
(deck de palestra), `/stats` (métricas da wiki), `/glossario` e `/ship`
(commit → main). Busca semântica local sobre as fontes via
[qmd](https://github.com/tobi/qmd); o lint roda no CI a cada push.

| Caminho | Conteúdo |
|---|---|
| `wiki/` | Páginas curadas (conceitos, obras, personalidades, questões, sínteses, aprofundamentos) — o que é publicado |
| `raw/` | Fontes ingeridas (Pentateuco, obras, transcrições) — excluído do build público |
| `.claude/` | Skills, rules condicionais e hooks que governam o workflow |
| `scripts/` | Build, lint, ingest e automações |

## Documentação

- **Propósito, tom e hierarquia de autoridade** → [`CLAUDE.md`](CLAUDE.md)
- **Roadmap e estado do projeto** → [`ROADMAP.md`](ROADMAP.md)
- **Setup numa máquina nova / migração** → [`docs/migracao.md`](docs/migracao.md)

## Direitos

O conteúdo curado e produzido nesta wiki está licenciado sob
[CC BY-NC-SA 4.0](LICENSE-CONTENT.md). A wiki cita obras de autores ainda
protegidos por direitos autorais (Chico Xavier, Divaldo, Hammed e outros)
exclusivamente para estudo e comentário; cada página de obra protegida indica,
quando possível, onde adquirir o texto completo.
