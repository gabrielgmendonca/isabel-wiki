# CEAK — auditoria final pós-conversão

Gerado em 2026-06-02. Catálogo de 356 PDFs do Centro Espírita Allan Kardec processado.

## Sumário

- **239** com `.md` em `raw/` (PDF baixado + convertido por marker) — 67%
- **62** match heurístico (já em `raw/` com slug diferente — não re-baixadas)
- **2** só PDF (conversão por marker falhou — OOM nos PDFs gigantes)
- **7** com link 404 no CEAK
- **46** em tier ambíguo (Pietro Ubaldi, Edgard Armond, Eduardo Penna, Hernani de Andrade) — não baixadas por padrão

**Cobertura útil (md + heurístico): 301/356 (84%)**

## Cobertura por autor

- ✓ **allan-kardec/kardec-pentateuco** — 5/5 (md:0 heur:5)
- ✓ **allan-kardec/kardec-biografias** — 4/4 (md:4 heur:0)
- ✓ **allan-kardec/kardec-complementares** — 9/9 (md:5 heur:4)
- ✓ **allan-kardec/kardec-revista** — 12/12 (md:0 heur:12)
- ✓ **arthur-conan-doyle/autor** — 2/2 (md:2 heur:0)
- ✓ **bezerra-de-menezes/autor** — 4/4 (md:4 heur:0)
- ✓ **cairbar-schutel/autor** — 18/18 (md:18 heur:0)
- ✓ **camille-flammarion/autor** — 12/12 (md:1 heur:11)
- ✓ **chico-xavier/medium:andre-luiz** — 19/19 (md:19 heur:0)
- ✓ **chico-xavier/medium:emmanuel** — 35/35 (md:31 heur:4)
- ✓ **chico-xavier/medium:humberto-de-campos** — 4/4 (md:3 heur:1)
- ✓ **chico-xavier/medium:irmao-x** — 10/10 (md:10 heur:0)
- ⚠ **divaldo-franco/medium:joanna-de-angelis** — 16/18 (md:1 heur:15)
    - *Estudos Espíritas* — 404 no CEAK
    - *Lições para a felicidade* — 404 no CEAK
- ✓ **divaldo-franco/medium:manoel-philomeno-de-miranda** — 15/15 (md:15 heur:0)
- ⚠ **gabriel-delanne/autor** — 10/12 (md:5 heur:5)
    - *Les Apparitions Matérialisées des Vivants & des Morts - Tome I - Les Fantômes de Vivants* — marker OOM (PDF gigante)
    - *Les Apparitions Matérialisées des Vivants & des Morts - Tome II - Les Apparitions des Morts* — marker OOM (PDF gigante)
- ⚠ **leon-denis/autor** — 18/20 (md:18 heur:0)
    - *Congresso Espírita de Liège-Bélgica (1905)* — 404 no CEAK
    - *O Espiritismo e as Forças Radiantes* — 404 no CEAK
- ✓ **pedro-de-camargo/autor** — 4/4 (md:4 heur:0)
- ✓ **canuto-abreu/autor** — 2/2 (md:2 heur:0)
- ✓ **carlos-alberto-baccelli/medium:inacio-ferreira** — 2/2 (md:2 heur:0)
- ✓ **ernesto-bozzano/autor** — 45/45 (md:40 heur:5)
- ✓ **feb/estudos-feb** — 4/4 (md:4 heur:0)
- ⚠ **herculano-pires/autor** — 34/37 (md:34 heur:0)
    - *Visão Espírita da Bíblia* — 404 no CEAK
    - *O Verbo e A Carne* — 404 no CEAK
    - *O Espírito e o Tempo* — 404 no CEAK
- ✓ **herminio-correa-de-miranda/autor** — 15/15 (md:15 heur:0)
- ✓ **inacio-ferreira/autor** — 2/2 (md:2 heur:0)

## Tier ambíguo — decisão editorial (2026-06-03)

**Nenhum dos 4 autores tier-ambíguo é ingerido na wiki**. Decisão revisada em 2026-06-03; aplicar a futuras revisões do catálogo CEAK.

| Autor | Obras | Razão |
|---|---|---|
| edgard-armond | 5 | Roustainguista. *Os Exilados da Capela* contradiz a Gênese kardequiana — fora de escopo. |
| pietro-ubaldi | 24 | Neoespiritismo sincrético (misticismo católico + esoterismo). *A Grande Síntese* não é psicografia kardecista — fora de escopo. |
| eduardo-penna | 9 | Autor contemporâneo de 'Espiritismo Científico'/'Pilares'/'Astrobiologia Espírita'. Não-consagrado, sem entrada na hierarquia oficial. |
| hernani-guimaraes-de-andrade | 8 | Pesquisador paranormal (Reencarnação no Brasil, PSI). Útil como escudo científico mas fora do canon kardecista estrito — não ingerir por padrão. |

Para opt-in pontual (obra específica), usar:

```bash
uv run python scripts/download_cealk.py --tier 9 --only <substring>
uv run python scripts/convert_cealk_batch.py --tier 9 --only <substring>
```

## Links 404 no CEAK

Obras listadas no catálogo mas com arquivo removido do servidor. Buscar em fonte alternativa:

- *Congresso Espírita de Liège-Bélgica (1905)* (leon-denis) — [link CEAK 404](https://livros.ceallankardec.org.br/Leon_Denis-02-Congresso%20Espirita%20Liege%20Bélgica%201905.pdf)
- *O Espiritismo e as Forças Radiantes* (leon-denis) — [link CEAK 404](https://livros.ceallankardec.org.br/Leon_Denis-09-O%20Espiritismo%20e%20as%20Forças%20Radiantes.pdf)
- *04 - Visão Espírita da Bíblia* (herculano-pires) — [link CEAK 404](https://extras.ceallankardec.org.br/HP_04_Visao_Espirita_da_Biblia.pdf)
- *06 - O Verbo e A Carne* (herculano-pires) — [link CEAK 404](https://livros.ceallankardec.org.br/HP_06_O_Verbo_e_A_Carne_(+JAF).pdf)
- *12 - O Espírito e o Tempo* (herculano-pires) — [link CEAK 404](https://livros.ceallankardec.org.br/HP_12_O_Espírito_e_O_Tempo.pdf)
- *18 -Estudos Espíritas* (divaldo-franco) — [link CEAK 404](https://livros.ceallankardec.org.br/DPF_JA-18-Estudos_Espíritas.pdf)
- *19 - Lições para a felicidade* (divaldo-franco) — [link CEAK 404](https://livros.ceallankardec.org.br/DPF_JA-19-Lições_para_a_felicidade.pdf)

## Próximos passos

1. **Match heurístico (62 obras)** — verificar que os slugs locais cobrem o que está no CEAK. Listei caso a caso na seção "Match heurístico" do tracker antigo (também em `data/cealk-catalogo.json`).
2. **Tier ambíguo** — revisar lista, decidir caso a caso. Hernani de Andrade (pesquisa científica do espiritismo) e Eduardo Penna podem ser úteis; Ubaldi/Armond requerem mais cautela editorial.
3. **Links 404** — tentar `scripts/download_espiritualidades_autor.py` ou Portal do Espírito para as 7 obras com link quebrado.
4. **Delanne PDFs gigantes** — para os 2 volumes franceses (111+116 MB), considerar conversão isolada com page_range fracionado: `./scripts/convert_pdf_to_md.sh <pdf> --page_range 0-200`.
5. **Curadoria via `/ingest`** — as 239 obras com `.md` estão em formato raw/. Próximo passo é criar páginas curadas em `wiki/obras/` para as obras prioritárias.
