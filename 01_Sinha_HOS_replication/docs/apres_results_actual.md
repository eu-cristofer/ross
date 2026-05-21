---
marp: true
theme: default
paginate: true
header: "Resultados atuais — Sinha (2007) replication pipeline"
footer: "Cristofer Antoni Souza Costa · POSMEC / UFU · 2026-05-21"
size: 16:9
style: |
  section { font-size: 23px; }
  section.lead h1 { font-size: 42px; }
  section.lead { text-align: center; }
  table { font-size: 19px; }
  pre { font-size: 17px; }
  h2 { color: #1f4e79; }
  .fig { background:#f5f7fa; border-left: 4px solid #1f4e79; padding: 8px 12px; font-size: 18px; }
  .source { color:#666; font-size: 16px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Resultados que já estão no repositório

## O que o *pipeline* de replicação de Sinha (2007) entrega **hoje**

**Cristofer Antoni Souza Costa**
*Mestrado em Engenharia Mecânica — POSMEC / UFU*
Orientador: Prof. Dr. Aldemir Aparecido Cavallini Junior

Data de referência: **2026-05-21**

---

# Como ler esta apresentação

Cada slide associa um **resultado verificável** (notebook executado,
módulo Python testado, constante exportada) a uma **figura sugerida** que
pode ser gerada *neste mesmo instante* pelo código já versionado. Nenhum
slide reporta valor numérico que não esteja em um artefato em disco.

A nomenclatura é:

- **Resultado** — o que existe e é executável em `01_Sinha_HOS_replication/`.
- **Figura sugerida** — a saída gráfica que o código atual produz; quando
  não há figura embutida no notebook, indica-se o *helper* de
  [`plot_utils.py`](../plot_utils.py) responsável.
- **Fonte** — caminho relativo para o artefato.

Para o relato narrativo paralelo (sprints concluídos vs. pendentes), ver
[`apres_validacao.md`](apres_validacao.md).

---

# Mapa dos resultados deste deck

| # | Resultado | Sprint | Slide |
|---|---|---|---|
| R1 | Calibração modal de `kxx` para `f₁ = 27,50 Hz` | 00 | 4 |
| R2 | Contrato de geometria persistido (`sinha_rotor.toml`) | 00 | 5 |
| R3 | Estimador de bi-espectro com normalização Kim–Powers | 01 | 6 |
| R4 | Teste positivo de QPC (`b² ≥ 0,95`) | 01 | 7 |
| R5 | Teste negativo de QPC (`b² ≤ 0,20`) | 01 | 8 |
| R6 | Tri-espectro esparso (limiar 0,10) | 01 | 9 |
| R7 | Comparação Mayes × Gasch × *open* — perfis `K(θ)` | — | 10 |
| R8 | Resposta ao desbalanceamento + varredura de fase 1X/2X/3X | — | 11 |
| R9 | Cadeia de aquisição Sinha-compatível parametrizada | 01 | 12 |
| R10 | Tutoriais didáticos de QPC (EN + PT-BR) | 01 | 13 |

---

# R1 — Calibração modal: `f₁ → 27,50 Hz`

O notebook [`00a_modal_check.ipynb`](../00a_modal_check.ipynb) carrega
[`sinha_rotor.toml`](../sinha_rotor.toml), executa `rotor.run_modal(speed=0)`
e converte `modal.wn / (2π)` em Hz. A célula A asserta a tolerância de
±0,05 Hz em torno de `SINHA_MODAL_TARGET = 27.50` Hz, valor exportado por
[`constants.py`](../constants.py) com base em Sinha (2007, §3) e Ewins
(2000). A rigidez `kxx = kyy` foi obtida em
[`00_sinha_rotor.ipynb`](../00_sinha_rotor.ipynb) por `scipy.optimize.brentq`
aplicado ao resíduo `f₁(k) − 27,50`.

<div class="fig">

**Figura sugerida 1.1 — Forma modal do primeiro modo flexural.**
Gerar com `rotor.run_modal(speed=0).plot_mode_2d(0)`
(API documentada em [`../CLAUDE.md`](../CLAUDE.md)).
Eixos: comprimento do eixo (m) × amplitude modal normalizada.

**Figura sugerida 1.2 — Tabela de resíduo da calibração.**
Saída da célula A: `f_hz[0]`, `|f_hz[0] − 27.50|`, status `PASS/FAIL`.

</div>

<span class="source">Fonte: [`00a_modal_check.ipynb`](../00a_modal_check.ipynb), [`constants.py`](../constants.py).</span>

---

# R2 — Contrato de geometria persistido

[`sinha_rotor.toml`](../sinha_rotor.toml) é o artefato congelado que
encerra o Sprint 00. Cada notebook a jusante chama
`rs.Rotor.load("sinha_rotor.toml")` e recebe a mesma topologia: nós de
mancal `BEARING_1_NODE = 1` e `BEARING_2_NODE = 11`, disco em
`DISK_NODE = 6`, trinca em `CRACK_NODE = 7`, sonda em `PROBE_NODE = 10`,
todos exportados por [`constants.py`](../constants.py).

A propagação é auditada por asserções em cascata (por exemplo,
`assert rotor.disk_elements[0].n == DISK_NODE`) recomendadas em
[`planejamento_modelagem_validacao.md`](planejamento_modelagem_validacao.md) §3.

<div class="fig">

**Figura sugerida 2.1 — Esquemático 2-D do rotor montado.**
Gerar com `rotor.plot_rotor()` da ROSS (Timbó et al., 2020) e sobrepor
marcadores nas posições de `BEARING_*_NODE`, `DISK_NODE`, `CRACK_NODE`,
`PROBE_NODE`. Já existem versões aproximadas dentro de
[`00_sinha_rotor.ipynb`](../00_sinha_rotor.ipynb).

**Figura sugerida 2.2 — Tabela de procedência das constantes.**
Recortar o *docstring* de [`constants.py`](../constants.py) que mapeia
símbolo → origem (Sinha §3, §5, decisões D-001/D-002).

</div>

<span class="source">Fonte: [`sinha_rotor.toml`](../sinha_rotor.toml), [`constants.py`](../constants.py), [`00_sinha_rotor.ipynb`](../00_sinha_rotor.ipynb).</span>

---

# R3 — Estimador de bi-espectro com normalização Kim–Powers

A função `signal_utils.bispectrum(x, fs, nfft, noverlap, window)`
implementa o estimador direto descrito por Collis, White & Hammond (1998)
com a normalização de Kim & Powers (1979) — `b² = |B|² / (⟨|X(f_l) X(f_m)|²⟩
⟨|X(f_l + f_m)|²⟩)`. O eixo é construído sobre a região não-redundante
`f_l ≤ f_m` e `f_l + f_m ≤ Nyquist`; valores de denominador abaixo de
`1·10⁻³⁰` são substituídos por esse piso para impedir divisão singular
(ver [`signal_utils.py`](../signal_utils.py) linhas 123–181).

Os defaults de Sinha (2007, §3.3) são herdados de
[`constants.py`](../constants.py): `nfft = 2048`, `noverlap = 1024`,
`Δf = 1,25 Hz`, 50 segmentos a `fs = 2560`.

<div class="fig">

**Figura sugerida 3.1 — Superfície |B|/max|B|.**
Gerar com `plot_utils.plotly_bispectrum_surface(B, freqs, fmax_hz=50)`
sobre o sinal de Teste A (slide R4). Triângulo não-redundante,
colorscale `Viridis`.

**Figura sugerida 3.2 — Superfície de bicoerência² (b² ∈ [0, 1]).**
Gerar com `plot_utils.plotly_bicoherence_surface(b2, freqs)`.

</div>

<span class="source">Fonte: [`signal_utils.py`](../signal_utils.py) (linhas 1–47, 123–181), [`plot_utils.py`](../plot_utils.py) (linhas 145–202).</span>

---

# R4 — Teste positivo: a QPC é detectada

[`06_hos_validation.ipynb`](../06_hos_validation.ipynb) constrói o sinal
sintético `x(t) = cos(2π f t) + 0,5 cos(2π·2f·t + 2φ) + 0,5 cos(2π·3f·t + 3φ)`
com `f = 12,5 Hz`, `fs = 2560 Hz`, `T = 25 s` e `φ = 1,3 rad`. Por
construção, as componentes em `2f` e `3f` carregam fase travada a `2φ` e
`3φ`, configurando acoplamento quadrático e cúbico de fase.

O critério de aceitação do Sprint 01 é `b²(f, f) ≥ 0,95` e
`b²(f, 2f) ≥ 0,95` no estimador `signal_utils.bispectrum`. A passagem
desse teste é a evidência de que a normalização e a média por segmento
estão corretas (Kim & Powers, 1979).

<div class="fig">

**Figura sugerida 4.1 — Espectro de amplitude do sinal de Teste A.**
`plot_utils.plotly_spectrum(amp, freqs, fmax_hz=80)`. Devem aparecer
três picos em `f`, `2f`, `3f`.

**Figura sugerida 4.2 — Superfície de bicoerência² do Teste A.**
`plot_utils.plotly_bicoherence_surface(b2, freqs, fmax_hz=50)`. O pico
sobre `(f, f)` e `(f, 2f)` deve saturar próximo de 1.

</div>

<span class="source">Fonte: [`06_hos_validation.ipynb`](../06_hos_validation.ipynb), [`sprints/01_hos_core.md`](../sprints/01_hos_core.md) §"Teste A".</span>

---

# R5 — Teste negativo: ruído faseado **não** é confundido com QPC

O mesmo notebook [`06_hos_validation.ipynb`](../06_hos_validation.ipynb)
constrói um sinal com **idêntico conteúdo espectral** ao de Teste A, mas
com fases reembaralhadas a cada bloco de 1 s. Por construção, o
acoplamento quadrático/cúbico é destruído sem alterar o periodograma.

O critério de aceitação é `max b² ≤ 0,20`. Esse é o teste decisivo: uma
implementação que normalize por `|X(f_l + f_m)|` *dentro* de cada
segmento, em vez de `⟨|X(f_l + f_m)|²⟩` agregado, falha aqui — e foi por
isso que o sprint 01 fez deste o teste falsificável principal
(Kim & Powers, 1979; Collis et al., 1998).

<div class="fig">

**Figura sugerida 5.1 — Superfície de bicoerência² do Teste B.**
`plot_utils.plotly_bicoherence_surface(b2_neg, freqs, fmax_hz=50)`. A
superfície deve permanecer rente ao chão (`b² ≲ 0,2`) em toda a região
não-redundante.

**Figura sugerida 5.2 — PSD de Welch dos dois sinais lado-a-lado.**
`signal_utils.psd_welch(...)` comparando Teste A vs. Teste B: os
periodogramas são quase indistinguíveis — o discriminador é o bi-espectro,
não o segundo momento.

</div>

<span class="source">Fonte: [`06_hos_validation.ipynb`](../06_hos_validation.ipynb), [`sprints/01_hos_core.md`](../sprints/01_hos_core.md) §"Teste B".</span>

---

# R6 — Tri-espectro esparso (T₁₁₁ acima do limiar)

`signal_utils.trispectrum(x, fs, ..., threshold=0.10)` devolve um
dicionário `{(l, m, n) → T_xxxx}` restrito à região
`l ≤ m ≤ n`, `l + m + n < Nyquist` e
`|T| / max|T| ≥ 0,10` — exatamente a convenção de Sinha (2007, Figs. 7–8).
A estrutura esparsa controla o custo de armazenamento O(N³) e produz
listas curtas, fáceis de auditar.

O Teste C do Sprint 01, em [`06_hos_validation.ipynb`](../06_hos_validation.ipynb),
exige que `(i_f, i_f, i_f)` apareça no dicionário com
`|T| / max|T| ≥ 0,95` e que a coleção total contenha ≤ 10 entradas — i.e.,
a esparsidade é parte do contrato.

<div class="fig">

**Figura sugerida 6.1 — Esferas do tri-espectro (Teste A).**
`plot_utils.plotly_trispectrum_balls(T_dict, freqs, fmax_hz=60, amp_min=0.10)`.
A esfera dominante deve cair sobre `(f, f, f)` com diâmetro normalizado
próximo de 1.

**Figura sugerida 6.2 — Listagem das chaves retidas.**
Tabela com colunas `(l, m, n)`, `f_l`, `f_m`, `f_n`, `|T|/max|T|`.

</div>

<span class="source">Fonte: [`signal_utils.py`](../signal_utils.py) linhas 190–257; [`plot_utils.py`](../plot_utils.py) linhas 204–254.</span>

---

# R7 — Trinca respirante: `K(θ)` Mayes × Gasch × *open*

O notebook [`03_sinha_crack_model_comparison.ipynb`](../03_sinha_crack_model_comparison.ipynb)
percorre o ciclo angular completo `θ ∈ [0, 2π]` para os três modelos de
respiração disponíveis na ROSS — Mayes (Mayes & Davies, 1984), Gasch
(Gasch, 1993) e *open*. A profundidade canônica é `CRACK_RATIO = 0.5`
(Sinha, 2007, §3), exportada por [`constants.py`](../constants.py).

A função geométrica de Mayes implementa `f(θ) = ½(1 − cos θ)`, equivalente
à forma `(1 − cos θ)·Δk/2` usada por Sinha (2007, §5) em seu próprio FE —
a justificativa explícita, em [D-003](DECISIONS.md), para Mayes ser o
**único** modelo da matriz de validação (Sprints 04–07).

<div class="fig">

**Figura sugerida 7.1 — `K(θ)[0, 0]` para os três modelos.**
Subplot com eixo `θ` em radianos e ordenada `K(θ)[0, 0] / K_intact[0, 0]`.
Mayes deve mostrar variação senoidal suave; Gasch, chaveamento descontínuo;
*open*, função degrau bloqueada.

**Figura sugerida 7.2 — Ângulo de abertura máxima `θ_open`.**
Marcador do mínimo de `K(θ)[0, 0]` (próximo de 180° para Mayes), conforme
verificação informativa proposta em [`sprints/00_modal_validation.md`](../sprints/00_modal_validation.md) §"Cell B".

</div>

<span class="source">Fonte: [`03_sinha_crack_model_comparison.ipynb`](../03_sinha_crack_model_comparison.ipynb), [`constants.py`](../constants.py), [`DECISIONS.md`](DECISIONS.md) D-003.</span>

---

# R8 — Desbalanceamento e harmônicos 1X / 2X / 3X

O notebook [`02_sinha_unbalance_phase_crack.ipynb`](../02_sinha_unbalance_phase_crack.ipynb)
executa varreduras determinísticas com `UNB_MAG = 2·10⁻⁴ kg·m` e
`UNB_PHASE = 4π/3 rad` (constantes canônicas; ver
[`constants.py`](../constants.py) e [D-002](DECISIONS.md)). O *helper*
[`sinha_helpers.get_harmonic_amplitude`](../sinha_helpers.py) extrai a
amplitude da FFT no *bin* mais próximo de cada harmônico após a janela
de regime permanente.

[`01b_unbalance.ipynb`](../01b_unbalance.ipynb) gera a linha de base sem
trinca, usada como controle para detectar a contribuição da componente
2X induzida pela respiração da trinca.

<div class="fig">

**Figura sugerida 8.1 — Espectro de amplitude no nó da sonda.**
`plot_utils.plotly_spectrum(amp, freqs, fmax_hz=80)` em 650 rpm e 750 rpm
(constantes `SPEED_CRACK_0`, `SPEED_CRACK_1`). Marcar 1X, 2X, 3X
manualmente.

**Figura sugerida 8.2 — Barras agrupadas das amplitudes 1X/2X/3X.**
Cores fixadas em `sinha_helpers.HARMONIC_COLORS`. Comparar caso saudável
× trinca a `a/D = 0,5` em cada velocidade.

**Figura sugerida 8.3 — Diagrama polar de fase.**
Construído com `probe_dof_indices` para extrair `dof_x`/`dof_y` corretos.

</div>

<span class="source">Fonte: [`02_sinha_unbalance_phase_crack.ipynb`](../02_sinha_unbalance_phase_crack.ipynb), [`01b_unbalance.ipynb`](../01b_unbalance.ipynb), [`sinha_helpers.py`](../sinha_helpers.py).</span>

---

# R9 — Cadeia de aquisição parametrizada (pronta para a Sprint 02)

Mesmo antes da campanha HDF5, o *pipeline* de pré-condicionamento de
sinais está completo e testável: `signal_utils.downsample_to` aplica um
Butterworth de oitava ordem em fase zero (`filtfilt`) com corte em
`SINHA_AA_CUTOFF_HZ = 1000` Hz, seguido por decimação inteira para a
taxa-alvo `SINHA_FS_HZ = 2560` Hz; `signal_utils.add_awgn` injeta ruído
gaussiano branco para um SNR-alvo, default `SNR_DB = 40` (Sinha, 2007,
§5).

Todos os números acima são **constantes nomeadas** em
[`constants.py`](../constants.py) — não há valor mágico inline em
notebook. A nota técnica
[`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md)
formaliza a cadeia para a seção de Métodos da dissertação.

<div class="fig">

**Figura sugerida 9.1 — Resposta em frequência do filtro AA.**
`scipy.signal.freqz` aplicado aos coeficientes retornados por
`butter(8, 1000/(2560/2), btype="low")`. Marcar a banda passante e o
ponto de –3 dB.

**Figura sugerida 9.2 — Sinal × sinal-com-ruído (zoom 0,5 s).**
Linha azul: sinal limpo; linha cinza: `add_awgn(x, snr_db=40)`. Mostrar
PSD lado a lado com `psd_welch`.

</div>

<span class="source">Fonte: [`signal_utils.py`](../signal_utils.py) linhas 278–310; [`constants.py`](../constants.py); [`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md).</span>

---

# R10 — Tutoriais de QPC: didática reproduzível

Para sustentar o discurso da banca e da defesa pública, dois notebooks
demonstram a leitura física do bi-espectro / bicoerência sobre sinais
sintéticos com QPC controlada:

- [`07_hos_demo.ipynb`](../07_hos_demo.ipynb) — demonstração em inglês,
  caminho técnico (sinais com fase travada vs. fase aleatória).
- [`08_hos_qpc_demo_ptbr.ipynb`](../08_hos_qpc_demo_ptbr.ipynb) — tutorial
  em português orientado a leitor não-especialista; cita explicitamente
  Sinha (2007), Kim & Powers (1979) e Collis et al. (1998).

Esses notebooks usam exclusivamente os mesmos *helpers* de
[`signal_utils.py`](../signal_utils.py) e [`plot_utils.py`](../plot_utils.py)
que serão empregados nos Sprints 04–06 — i.e., o que aparece nas figuras
da defesa é, literalmente, o mesmo código que gera as figuras da matriz
de validação.

<div class="fig">

**Figura sugerida 10.1 — Composição didática.**
Subplot 2×2: (a) sinal no tempo, (b) espectro de amplitude, (c)
bicoerência², (d) tri-espectro em esferas — todos extraídos do notebook
07 / 08.

</div>

<span class="source">Fonte: [`07_hos_demo.ipynb`](../07_hos_demo.ipynb), [`08_hos_qpc_demo_ptbr.ipynb`](../08_hos_qpc_demo_ptbr.ipynb).</span>

---

# Quadro de figuras pronto para o slide-deck da defesa

| Tag | Conteúdo | Notebook / helper | Tipo |
|---|---|---|---|
| F1.1 | Forma do primeiro modo flexural | [`01a_sinha_rotor_modal.ipynb`](../01a_sinha_rotor_modal.ipynb) + `plot_mode_2d` | 2-D linha |
| F2.1 | Esquemático do rotor montado | [`00_sinha_rotor.ipynb`](../00_sinha_rotor.ipynb) + `rotor.plot_rotor()` | 2-D |
| F3.1 | Superfície \|B\|/max\|B\| (Teste A) | [`06_hos_validation.ipynb`](../06_hos_validation.ipynb) + `plotly_bispectrum_surface` | 3-D Plotly |
| F4.2 | Bicoerência² Teste A | mesmo notebook + `plotly_bicoherence_surface` | 3-D Plotly |
| F5.1 | Bicoerência² Teste B (negativo) | mesmo notebook | 3-D Plotly |
| F6.1 | Esferas do tri-espectro | mesmo notebook + `plotly_trispectrum_balls` | 3-D Plotly |
| F7.1 | `K(θ)` Mayes/Gasch/open | [`03_sinha_crack_model_comparison.ipynb`](../03_sinha_crack_model_comparison.ipynb) | 2-D linha |
| F8.1 | Espectro de amplitude da sonda | [`02_sinha_unbalance_phase_crack.ipynb`](../02_sinha_unbalance_phase_crack.ipynb) + `plotly_spectrum` | 2-D linha |
| F8.2 | Barras 1X/2X/3X (saudável vs. trinca) | mesmo notebook + `sinha_helpers.HARMONIC_COLORS` | 2-D barra |
| F9.1 | Resposta do filtro AA Butterworth | reproduzir de `signal_utils.downsample_to` | 2-D linha |

---

# Resultados **ainda não disponíveis** (transparência metodológica)

O *pipeline* corrente **não** produz, nesta data, os seguintes resultados,
todos atribuídos a sprints posteriores em [`PLAN.md`](PLAN.md) §2:

- Bi-espectro / tri-espectro a partir de registros de 25 s do FE (Sprint 02).
- Calibração de amortecimento `ζ₁ = 0,3 %` e tabela de convergência de
  `NUM_MODES` (Sprint 03).
- Replicação numérica das Figs. 9 e 10 de Sinha (Sprint 04).
- Topologia B₂₂ × B₁₁ para trinca a 650 / 750 rpm e T₂₂₂ a 750 rpm
  (Sprint 05).
- Topologia B₁₃ presente × B₂₂ ausente para desalinhamento a 750 / 900 rpm
  (Sprint 06) — a **contribuição original** relativa a Sinha (2007, §5).
- Matriz consolidada das dez reivindicações falsificáveis (Sprint 07,
  arquivo-alvo `results/validation_matrix.csv`).

Nenhuma figura desses sprints é incluída neste deck. Reportar resultados
ainda não computados violaria a política de silêncio factual adotada no
projeto.

---

# Como reproduzir todos os resultados deste deck

```bash
# A partir da raiz do repositório
pip install -e ".[dev]"

# A partir de 01_Sinha_HOS_replication/
jupyter lab
```

A ordem de execução para regerar **todas** as figuras sugeridas:

```
00_sinha_rotor.ipynb                 → grava sinha_rotor.toml
00a_modal_check.ipynb                → F1.1, F2.1
01a_sinha_rotor_modal.ipynb          → F1.1 (alternativo)
01b_unbalance.ipynb                  → F8.1 baseline
02_sinha_unbalance_phase_crack.ipynb → F8.1, F8.2, F8.3
03_sinha_crack_model_comparison.ipynb→ F7.1
06_hos_validation.ipynb              → F3.1, F4.2, F5.1, F6.1
07_hos_demo.ipynb                    → F10.1 (EN)
08_hos_qpc_demo_ptbr.ipynb           → F10.1 (PT-BR)
```

A ordem reflete o grafo de dependência de [`sprints/README.md`](../sprints/README.md) §"Execution order".

---

# Síntese — onde o pipeline já entrega

A camada de **núcleo** está fechada e testada: rotor calibrado em
27,50 Hz (Sinha, 2007, §3), estimadores HOS auditados por testes
positivo / negativo / esparsidade contra a normalização de Kim & Powers
(1979), e cadeia de aquisição Sinha-compatível parametrizada por
constantes nomeadas com procedência rastreável.

A camada de **resultados de produção** — bi- e tri-espectros sobre
registros longos do FE com trinca e desalinhamento — depende da
materialização do `results/campaign.h5` (Sprint 02) e do amortecimento
proporcional `ζ₁ = 0,3 %` (Sprint 03). Esses sprints são, hoje, a fila
imediata.

Esta apresentação cobre, portanto, o que pode ser **mostrado, executado
e auditado em 2026-05-21**, sem antecipar o que pertence a Sprints
futuros.

---

# Referências

Collis, W. B., White, P. R., & Hammond, J. K. (1998). Higher-order spectra:
The bispectrum and trispectrum. *Mechanical Systems and Signal Processing*,
12(3), 375–394.

Ewins, D. J. (2000). *Modal testing: Theory, practice and application*
(2nd ed.). Research Studies Press.

Gasch, R. (1993). A survey of the dynamic behaviour of a simple rotating
shaft with a transverse crack. *Journal of Sound and Vibration*, 160(2),
313–332.

Kim, Y. C., & Powers, E. J. (1979). Digital bispectral analysis and its
applications to nonlinear wave interactions. *IEEE Transactions on Plasma
Science*, 7(2), 120–131.

Mayes, I. W., & Davies, W. G. R. (1984). Analysis of the response of a
multi-rotor-bearing system containing a transverse crack in a rotor.
*Journal of Vibration, Acoustics, Stress and Reliability in Design*,
106(1), 139–145.

---

# Referências (continuação)

Sinha, J. K. (2007). Higher order spectra for crack and misalignment
identification in the shaft of a rotating machine. *Structural Health
Monitoring*, 6(4), 325–334.

Timbó, R., Martins, R., Bachmann, G., Rangel, F., Mota, J., Valério, J.,
& Ritto, T. G. (2020). ROSS — Rotordynamic Open Source Software.
*Journal of Open Source Software*, 5(48), 2120.

Xia, Y., Pang, J., Yang, L., Zhao, Q., & Yang, X. (2019). Study on
vibration response and orbits of misaligned rigid rotors connected by
hexangular flexible coupling. *Applied Acoustics*, 155, 286–296.

---

<!-- _class: lead -->

# Contato

**Cristofer Antoni Souza Costa**
*Mestrado em Engenharia Mecânica — POSMEC / UFU*

cristofercosta@yahoo.com.br

Snapshot do repositório: `01_Sinha_HOS_replication/` em **2026-05-21**.
