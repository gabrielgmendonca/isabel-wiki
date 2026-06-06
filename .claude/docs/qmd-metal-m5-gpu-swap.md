# Caminho 2 — destravar a GPU (Metal) do `qmd embed` no M5 trocando os dylibs à mão

> **Status:** experimental, **não testado**. Risco real de ABI (ver §6). Faça com calma, com backup, e
> só persista se o gate de símbolos (§5.4) passar. Caminho recomendado continua sendo o 1 (esperar a
> `node-llama-cpp` empacotar um llama.cpp ≥ `b?` com o fix #18456). Este doc é o plano B.

## 1. O problema (resumo)

`qmd embed` cai pra **CPU** porque a compilação on-the-fly dos shaders Metal falha no M5:

```
[node-llama-cpp] ggml_metal_library_init_from_source: error compiling source
```

Causa-raiz: o build empacotado é o llama.cpp **`b8390`**. No M5 (`MTLGPUFamilyApple10` / Metal 4) o
`#ifdef GGML_METAL_HAS_TENSOR` fica **definido**, então o source Metal inclui os kernels cooperativos
**BF16×F16**, que estouram o `static_assert "Input types must match cooperative tensor types"
(__is_same_v<bfloat, half>)` contra os headers `MetalPerformancePrimitives` do macOS 26.x. O `b8390`
**não tem** a env var de escape `GGML_METAL_DISABLE_TENSOR_API` (verificado: `strings ... | grep -c` = 0)
nem o fix upstream **#18456** (que remove esses kernels, merged 31/dez/2025). Ambos são posteriores ao
`b8390`. Detalhes na memória `qmd-embed-cpu-truncation.md`.

A ideia do caminho 2: **manter o `llama-addon.node` do `b8390`** (não recompilar nada da node-llama-cpp —
foi isso que falhou antes, por quebras de API no `addon.cpp`) e **substituir apenas as bibliotecas
`libggml*`/`libllama` por um build novo do llama.cpp** que tenha o fix, renomeando-as para os nomes que
o addon espera.

## 2. Anatomia da pasta de binários

Pasta (o `qmd` instalado globalmente via npm):

```
/opt/homebrew/lib/node_modules/@tobilu/qmd/node_modules/@node-llama-cpp/mac-arm64-metal/bins/mac-arm64-metal/
```

Conteúdo e papel de cada arquivo:

| Arquivo | Papel | Substituir? |
|---|---|---|
| `llama-addon.node` | addon N-API (compilado contra a API do `b8390`) | **NÃO** — é o que define o ABI a respeitar |
| `libllama.metal.b8390.dylib` | biblioteca `llama` | sim ← `libllama.dylib` novo |
| `libggml.metal.b8390.dylib` | umbrella `ggml` (fina) | sim ← `libggml.dylib` novo |
| `libggml-base.dylib` | núcleo `ggml` | sim ← `libggml-base.dylib` novo |
| `libggml-metal.so` | **backend Metal — é AQUI que está o bug** | sim ← `libggml-metal.dylib` novo |
| `libggml-cpu.so` | backend CPU | sim ← `libggml-cpu.dylib` novo |
| `libggml-blas.so` | backend BLAS | sim ← `libggml-blas.dylib` novo |
| `_nlcBuildMetadata.json` | metadados (diz `release: "b8390"`) | opcional |

Fatos de linkagem que ditam o procedimento (apurados com `otool`/`nm`):

- **rpath do addon = `@loader_path`** → todos os dylibs têm que ficar **nesta mesma pasta**.
- O addon referencia, por `@rpath`, os nomes **versionados**: `libllama.metal.b8390.dylib`,
  `libggml.metal.b8390.dylib`, `libggml-base.dylib`. → renomear os dylibs novos para **exatamente**
  esses nomes evita ter que patchar (e reassinar) o `llama-addon.node`.
- Cadeia de dependência: `llama-addon.node` → `libllama.metal.b8390.dylib` → `libggml.metal.b8390.dylib`
  + `libggml-base.dylib`; `libggml-metal.so` → `libggml-base.dylib`.
- Os backends (`libggml-*.so`) são carregados em runtime via `ggml_backend_load_all_from_path`
  (registry dinâmico do ggml), por isso a extensão `.so` e não `.dylib` — **mantenha os nomes `.so`**.
- Tudo é assinado **adhoc / linker-signed**. Qualquer `install_name_tool` **invalida a assinatura** →
  re-assinar ad-hoc é obrigatório (§5.3), senão o loader recusa (`code signature invalid`).

## 3. Pré-requisitos

- Xcode Command Line Tools (`xcode-select --install`) — para `metal`/`clang`/`codesign`.
- `cmake` (`brew install cmake`).
- Espaço e ~15-30 min de build.

## 4. Build do llama.cpp (só as libs, com cmake puro)

> Importante: **não** usar `node-llama-cpp source build`. Aqui usamos o cmake do upstream direto, então
> as quebras de API da node-llama-cpp 3.18.1 contra builds novos **não importam** (não recompilamos o addon).

Escolha do tag: o menor release que **contenha o fix #18456** (merged 31/dez/2025), para minimizar a
deriva de ABI em relação ao `b8390`. Verifique que o fix está presente antes de buildar.

```bash
cd ~/src   # onde preferir
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Conferir que o fix #18456 já está no ponto que você vai usar (commit "Metal: remove BF16 x F16 kernels"):
git log --oneline | grep -iE "bf16.*f16|18456|cooperative tensor" | head
# Faça checkout do tag/commit escolhido (>= o merge acima). Ex.: git checkout bXXXX

# Build shared libs com Metal:
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DGGML_METAL=ON \
  -DGGML_METAL_EMBED_LIBRARY=OFF \
  -DGGML_NATIVE=ON \
  -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_SERVER=OFF
cmake --build build --config Release -j

# As libs saem em build/bin/ (ou build/src + build/ggml/src dependendo da versão):
find build -name "libllama*.dylib" -o -name "libggml*.dylib" | sort
```

Você deve obter (nomes upstream): `libllama.dylib`, `libggml.dylib`, `libggml-base.dylib`,
`libggml-cpu.dylib`, `libggml-metal.dylib`, `libggml-blas.dylib` (este pode não existir; ok).

## 5. Trocar à mão

### 5.1 Backup (obrigatório)

```bash
BINS=/opt/homebrew/lib/node_modules/@tobilu/qmd/node_modules/@node-llama-cpp/mac-arm64-metal/bins/mac-arm64-metal
cp -a "$BINS" "$BINS.bak-b8390"     # backup completo da pasta
```

### 5.2 Copiar com os nomes que o addon espera

Ajuste `SRC` para a pasta onde as libs novas saíram (ex.: `build/bin`):

```bash
SRC=~/src/llama.cpp/build/bin

# umbrella, base, llama → nomes versionados .metal.b8390 (o que o addon procura)
cp "$SRC/libggml.dylib"        "$BINS/libggml.metal.b8390.dylib"
cp "$SRC/libggml-base.dylib"   "$BINS/libggml-base.dylib"
cp "$SRC/libllama.dylib"       "$BINS/libllama.metal.b8390.dylib"

# backends → manter extensão .so
cp "$SRC/libggml-metal.dylib"  "$BINS/libggml-metal.so"
cp "$SRC/libggml-cpu.dylib"    "$BINS/libggml-cpu.so"
[ -f "$SRC/libggml-blas.dylib" ] && cp "$SRC/libggml-blas.dylib" "$BINS/libggml-blas.so"
```

### 5.3 Corrigir install names + reassinar ad-hoc

Os dylibs novos têm `@rpath/libggml.dylib` etc.; precisam apontar para os nomes versionados:

```bash
cd "$BINS"

# IDs:
install_name_tool -id @rpath/libggml.metal.b8390.dylib   libggml.metal.b8390.dylib
install_name_tool -id @rpath/libllama.metal.b8390.dylib  libllama.metal.b8390.dylib

# Referências cruzadas (libllama e o umbrella apontavam pro libggml.dylib "cru"):
install_name_tool -change @rpath/libggml.dylib @rpath/libggml.metal.b8390.dylib libllama.metal.b8390.dylib
install_name_tool -change @rpath/libggml.dylib @rpath/libggml.metal.b8390.dylib libggml.metal.b8390.dylib 2>/dev/null || true

# (libggml-base.dylib mantém o nome → nada a mudar nas refs a ele.
#  Confira cada arquivo com: otool -L <arq> | grep rpath  — não pode sobrar @rpath/libggml.dylib)
for f in *.dylib *.so; do echo "== $f =="; otool -L "$f" | grep -E "@rpath/libggml(\.dylib|-)" ; done

# install_name_tool quebra a assinatura → reassinar ad-hoc TODOS:
codesign --force --sign - libggml-base.dylib libggml.metal.b8390.dylib libllama.metal.b8390.dylib \
                           libggml-metal.so libggml-cpu.so libggml-blas.so 2>/dev/null
codesign --verify --verbose libllama.metal.b8390.dylib   # deve dizer "valid on disk"
```

> Se em algum momento você decidir patchar o `llama-addon.node` em vez de renomear (não recomendado),
> ele **também** precisa de `codesign --force --sign -` depois — e aí qualquer mismatch derruba o carregamento.

### 5.4 GATE de símbolos (go/no-go) — faça ANTES de testar de verdade

O addon importa 152 símbolos `llama_`/`ggml_`, **incluindo C++ mangled internos** (ex.:
`llama_grammar_init_impl`) que **não** são API C estável. Se o build novo mudou alguma assinatura, o
símbolo some → o addon não carrega. Cheque que **todos** os símbolos importados existem nas libs novas:

```bash
cd "$BINS"
comm -23 \
  <(nm -u llama-addon.node | grep -E '_(llama|ggml)' | sort -u) \
  <(cat <(nm -gU libllama.metal.b8390.dylib) \
        <(nm -gU libggml.metal.b8390.dylib) \
        <(nm -gU libggml-base.dylib) \
        <(nm -gU libggml-cpu.so) <(nm -gU libggml-metal.so) \
     | awk '{print $NF}' | sort -u)
```

- **Saída vazia** → todos resolvem → pode testar (§5.5).
- **Saída não-vazia** → ABI incompatível (símbolos faltando listados). **Aborte**, restaure o backup
  (§7) e fique no CPU, ou tente um tag mais próximo do `b8390`.

### 5.5 Testar

```bash
qmd status                       # baseline
qmd embed -c wiki 2>&1 | head -5 # NÃO deve mais aparecer "error compiling source"
```

Sinais de sucesso: o erro `ggml_metal_library_init_from_source: error compiling source` **sumiu**, o
embed roda **muito mais rápido** (GPU ~ várias x a CPU), e `qmd status`/Activity Monitor mostram a GPU
ativa durante o embed. Se em vez disso o `qmd` **crashar no load** (`dyld: Symbol not found` /
`code signature invalid`), o gate §5.4 ou a reassinatura §5.3 não passaram → restaure o backup.

## 6. Riscos (por que isto pode não funcionar)

1. **ABI C++ interno.** O addon `b8390` importa símbolos C++ mangled de `llama`/`ggml` (grammar impl,
   etc.). Entre `b8390` e o tag novo, qualquer mudança de assinatura nesses símbolos = falha de load.
   É o motivo de existir o gate §5.4. Quanto mais novo o tag, maior a deriva — por isso pegar o
   **menor** tag que tenha o #18456.
2. **ABI binário do registry de backend.** `libggml-base` (núcleo) e os backends `.so` têm que vir do
   **mesmo build** (a interface base↔backend muda sem aviso). Nunca misture um `libggml-metal.so` novo
   com um `libggml-base.dylib` antigo, ou vice-versa.
3. **Re-embed.** Trocar dylib **não** muda a versão do `qmd` nem o `embed_fingerprint`, então **não**
   força re-embed. Mas se você trocar a versão do `qmd` depois, aí sim re-embeda (ver memória).
4. **Atualização do `qmd`/npm reverte tudo.** `npm i -g @tobilu/qmd@...` reescreve a pasta `bins/`.
   Após qualquer update do qmd, refazer a troca (ou o update já pode trazer o fix — checar primeiro).
5. **Truncagem.** Embed em CPU é lento e a janela de interrupção causa docs truncados (bug conhecido).
   Se a GPU passar a funcionar, esse risco cai junto.

## 7. Rollback

```bash
BINS=/opt/homebrew/lib/node_modules/@tobilu/qmd/node_modules/@node-llama-cpp/mac-arm64-metal/bins/mac-arm64-metal
rm -rf "$BINS" && mv "$BINS.bak-b8390" "$BINS"      # restaura o b8390 intacto
```

Ou, se não tiver o backup: `npm i -g @tobilu/qmd@2.5.3 --force` (reinstala os binários `b8390`).

## 8. Referências

- llama.cpp #17986 — `[metal] "Input types must match cooperative tensor types"` (issue canônica)
- llama.cpp #18456 — fix (remove kernels BF16×F16), merged 31/dez/2025
- llama.cpp #16634 — Metal4 tensor API + env var `GGML_METAL_DISABLE_TENSOR_API`
- Memória do projeto: `qmd-embed-cpu-truncation.md`
