---
paths:
  - ".claude/skills/**"
  - "scripts/**"
---

# Scripts e automação

- **Onde mora**: auxiliar de skill → `.claude/skills/<skill>/scripts/`; pipeline/curadoria reusada fora de skill → `scripts/`.
- **Como rodar**: sempre `uv run python <script>` (nem `python` nem `python3`). Exceção: no CI (`.github/workflows/*`) é `python3` — não mudar.
- **Lib madura > wrapper caseiro**: para HTML↔MD, YAML/TOML, slugify, datas etc., propor `uv add <pkg>` antes de escrever parser próprio de ~30+ linhas.
- **Conversores já existentes** (checar `ls scripts/convert_*` antes de criar outro):
  - `.doc`/`.docx` → `uv run python scripts/convert_doc_to_md.py <dir>`
  - `.pdf` → `./scripts/convert_pdf_to_md.sh <arquivo.pdf>` (`marker`; `USE_LLM=1` para layout sujo, exige `GEMINI_API_KEY` no `.env`). **Não** usar markitdown para PDF.
  - `.epub` → `uv run python scripts/convert_epub_to_md.py <arquivo-ou-dir>`; depois `scripts/normalize_raw_layout.py` para o layout de `raw/`.
  - YouTube → `/yt` ou `/yt-bulk`, nunca conversor genérico.
- **Lint em automação** (hooks, loops, `/ship`): o script `.claude/skills/lint/scripts/lint_wiki.py`, nunca a skill `/lint` (que usa LLM).
