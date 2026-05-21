---
marp: true
theme: default
paginate: true
header: "Diagnóstico de Falhas em Rotores via HOS — Replicação Numérica de Sinha (2007)"
footer: "Cristofer Antoni Souza Costa · POSMEC / UFU · 2026-05-21"
size: 16:9
style: |
  section { font-size: 24px; }
  section.lead h1 { font-size: 44px; }
  section.lead { text-align: center; }
  table { font-size: 20px; }
  pre { font-size: 18px; }
  h2 { color: #1f4e79; }
  .small { font-size: 18px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Modelagem Numérica e Validação — o que já existe no repositório

## Estado atual da replicação computacional de Sinha (2007)

**Cristofer Antoni Souza Costa**
*Mestrado em Engenharia Mecânica — POSMEC / UFU*
Orientador: Prof. Dr. Aldemir Aparecido Cavallini Junior

Data de referência: **2026-05-21**

---

# Como ler esta apresentação

Esta apresentação é um relato do **estado verificável** do diretório
[`01_Sinha_HOS_replication/`](../) na data acima. Cada afirmação remete a
um artefato no disco — notebook, módulo Python ou arquivo TOML — citado
de forma inline para que o revisor possa abri-lo e auditar.

O plano completo do objetivo específico §3.2 vive em
[`planejamento_modelagem_validacao.md`](planejamento_modelagem_validacao.md);
o painel ativo de progresso e bloqueios vive em [`PLAN.md`](PLAN.md);
o registro arquitetural das decisões vive em [`DECISIONS.md`](DECISIONS.md).
A presente narrativa **subordina-se** a esses documentos: descreve o que já
foi codificado, não o que está planejado.

---

# Painel de progresso (Sprints 00–07)

| Sprint | Título | Estado | Artefato verificável |
|---|---|---|---|
| 00 | Validação modal FE × Sinha §3/§5 | **concluído** | [`00a_modal_check.ipynb`](../00a_modal_check.ipynb), `SINHA_MODAL_TARGET = 27.50` Hz em [`constants.py`](../constants.py) |
| 01 | Núcleo HOS + validação sintética | **concluído** | [`signal_utils.py`](../signal_utils.py), [`plot_utils.py`](../plot_utils.py), [`06_hos_validation.ipynb`](../06_hos_validation.ipynb), [`07_hos_demo.ipynb`](../07_hos_demo.ipynb), [`08_hos_qpc_demo_ptbr.ipynb`](../08_hos_qpc_demo_ptbr.ipynb) |
| 02 | Aquisição Sinha-compatível + HDF5 | **em curso** | `run_campaign.py` e `results/campaign.h5` ainda não materializados (ver [`PLAN.md`](PLAN.md) §1) |
| 03 | Amortecimento ζ₁ = 0,3 % + truncamento modal | não iniciado | — |
| 04 | Replicação FE-FE das Figs. 9 e 10 de Sinha | não iniciado | — |
| 05 | HOS de trinca a 650/750 rpm | não iniciado | — |
| 06 | HOS de desalinhamento a 750/900 rpm (novo) | não iniciado | — |
| 07 | Matriz de validação + rascunho de Métodos | não iniciado | — |

Fonte: [`README.md`](../README.md) §"Status at a glance" e [`docs/PLAN.md`](PLAN.md) §2.

---

# Arquitetura computacional consolidada

Toda a cadeia de simulação está organizada em torno de **um contrato de
geometria congelado** e **uma única fonte de verdade de parâmetros**:

- **Modelo FE** — biblioteca [ROSS](../../ross/) (Timbó et al., 2020),
  com `ShaftElement` Euler–Bernoulli, efeitos giroscópicos e inércia
  rotativa habilitados por padrão da biblioteca.
- **Contrato de geometria** — [`sinha_rotor.toml`](../sinha_rotor.toml),
  gerado por [`00_sinha_rotor.ipynb`](../00_sinha_rotor.ipynb) e carregado
  via `rs.Rotor.load(...)` por todos os notebooks a jusante. Sua retomada
  exige edição explícita do notebook 00 e registro em
  [`DECISIONS.md`](DECISIONS.md).
- **Fonte única de parâmetros** — [`constants.py`](../constants.py),
  estabelecida na Sprint 01 (Pattern A). Notebooks importam constantes em
  vez de redefini-las. O *docstring* do módulo carrega a tabela de
  procedência símbolo-a-símbolo.

---

# Sprint 00 — validação modal (concluída)

Implementada em [`00a_modal_check.ipynb`](../00a_modal_check.ipynb),
seguindo a decisão arquitetural [D-001](DECISIONS.md) registrada em
2026-04-23.

A rigidez direcional dos mancais (`kxx = kyy`) é calibrada por
`scipy.optimize.brentq` aplicado ao resíduo `f₁(k) − 27,50 Hz` durante a
construção do rotor em [`00_sinha_rotor.ipynb`](../00_sinha_rotor.ipynb).
O alvo `SINHA_MODAL_TARGET = 27.50` Hz reproduz a resposta a impulso
experimental relatada por Sinha (2007, §3, obtida pelo método de Ewins,
2000), com tolerância de ±0,05 Hz. O valor de FE próprio de Sinha
(26,53 Hz, §5) **não é** o alvo — é apenas referência qualitativa para a
Fig. 10 (Sinha, 2007).

A célula A do notebook 00a converte `modal.wn / (2π)` em Hz e exige
`abs(f_hz[0] − 27.50) ≤ 0.05` como pré-condição bloqueante para todos os
sprints posteriores.

---

# Modelagem da falha: trinca respirante

A formulação Mayes–Davies (Mayes & Davies, 1984) está disponível na ROSS
e foi exercitada em
[`03_sinha_crack_model_comparison.ipynb`](../03_sinha_crack_model_comparison.ipynb),
que confronta os perfis `K(θ)` dos modelos Mayes, Gasch (1993) e *open*.

A função geométrica adotada é `f(θ) = ½(1 − cos θ)`, equivalente à forma
`(1 − cos θ)·Δk/2` citada por Sinha (2007, §5). A razão de profundidade
canônica do programa de validação é `CRACK_RATIO = 0.5`, exportada por
[`constants.py`](../constants.py) e justificada em
[D-003](DECISIONS.md) — Mayes é o **único** modelo da matriz de
validação Sprints 04–07; Gasch e *open* permanecem como referência
metodológica no notebook 03.

A verificação quantitativa de queda modal para 26,25 Hz na configuração
totalmente aberta (Sinha, 2007, §3) está agendada para a Sprint 04 e
**ainda não foi executada** — o sprint 00 limita-se a inspecionar o
perfil `K(θ)`.

---

# Modelagem da falha: desalinhamento (contribuição prevista)

A interface ROSS `rotor.run_misalignment(coupling="flex", mis_type="parallel")`,
implementando o acoplamento flexível hexagonal de Xia et al. (2019), está
disponível na biblioteca e é exercitada em
[`04_sinha_fault_analysis.ipynb`](../04_sinha_fault_analysis.ipynb)
(notebook tratado como *legacy* — ver [`code_review.md`](../code_review.md)
e [`PLAN.md`](PLAN.md) §3, item P1).

Os parâmetros do desalinhamento estão fixados em [`constants.py`](../constants.py):
`MIS_X = Q_(1.0e-3, "m")`, `MIS_Y = Q_(0.5e-3, "m")`,
`SPEED_MIS_0 = 750 rpm`, `SPEED_MIS_1 = 900 rpm`.

A originalidade declarada relativamente a Sinha (2007, §5 — *"the force
function due to the shaft misalignment is not well stood"*) está registrada
em [D-008 / sprints/README.md](../sprints/README.md). A validação
quantitativa (B₁₃ presente, B₂₂ ausente, T₁₁₁ único) **está agendada para
a Sprint 06** e ainda não foi executada.

---

# Sprint 01 — núcleo HOS (concluída)

O módulo [`signal_utils.py`](../signal_utils.py) implementa o estimador
direto de Collis, White & Hammond (1998) com a normalização de Kim &
Powers (1979). As funções principais já disponíveis:

- `bispectrum(x, fs, nfft, noverlap, window)` — retorna `B`, `b²` e o
  eixo de frequência; restringe a saída à região não-redundante
  `f_l ≤ f_m` e `f_l + f_m ≤ Nyquist`.
- `bicoherence(x, fs, ...)` — alias que devolve apenas `(b², freqs)`.
- `trispectrum(x, fs, ..., threshold=0.10)` — estimador esparso
  reproduzindo a convenção de Sinha (2007, Figs. 7–8) de plotar apenas
  amplitudes acima de 0,10.
- `amplitude_spectrum`, `window_and_detrend`, `psd_welch`,
  `harmonic_amplitude` — utilitários espectrais com correção de janela
  Hann.
- `downsample_to`, `add_awgn` — pré-condicionamento de sinais.

Os defaults `nfft = int(fs / SINHA_HOS_DF_HZ)` e
`noverlap = int(nfft · SINHA_HOS_OVERLAP)` reproduzem, para `fs = 2560`,
os 2048 pontos / 50 % de sobreposição / Δf = 1,25 Hz de Sinha (2007, §3.3).

---

# Sprint 01 — validação sintética dos estimadores

A correção do núcleo HOS foi verificada por três testes falsificáveis em
[`06_hos_validation.ipynb`](../06_hos_validation.ipynb), conforme
detalhado em [`sprints/01_hos_core.md`](../sprints/01_hos_core.md):

- **Teste A — positivo (QPC imposta).** Sinal `cos(2πft) + 0,5·cos(2π·2f·t + 2φ)
  + 0,5·cos(2π·3f·t + 3φ)` deve produzir `b²(f,f) ≥ 0,95` e `b²(f,2f) ≥ 0,95`.
- **Teste B — negativo (fases independentes por segmento).** Mesmo conteúdo
  espectral, mas fases recortadas por bloco; o estimador correto deve
  retornar `max b² ≤ 0,20`. Este é o teste que distingue uma implementação
  válida de uma com normalização errada por segmento.
- **Teste C — tri-espectro esparso.** A entrada `(i_f, i_f, i_f)` deve
  estar no dicionário retornado com `|T|/T_max ≥ 0,95` e o dicionário
  inteiro deve conter no máximo dez entradas acima do limiar 0,1.

Notebooks acessórios [`07_hos_demo.ipynb`](../07_hos_demo.ipynb) e
[`08_hos_qpc_demo_ptbr.ipynb`](../08_hos_qpc_demo_ptbr.ipynb) demonstram
o uso dos estimadores sobre sinais sintéticos com QPC controlada.

---

# Pipeline de aquisição (parâmetros já fixados)

A cadeia de amostragem alvo de Sinha (2007, §3) está codificada como
constantes do módulo [`constants.py`](../constants.py):

| Parâmetro | Símbolo | Valor | Origem |
|---|---|---|---|
| Frequência de aquisição | `SINHA_FS_HZ` | 2560 Hz | Sinha (2007) §3 |
| Corte do filtro anti-alias | `SINHA_AA_CUTOFF_HZ` | 1000 Hz | Sinha (2007) §3 |
| Resolução do bi-espectro | `SINHA_HOS_DF_HZ` | 1,25 Hz | Sinha (2007) §3.3 |
| Segmentos do estimador | `SINHA_HOS_N_SEGMENTS` | 50 | Sinha (2007) §3.3 |
| Sobreposição entre segmentos | `SINHA_HOS_OVERLAP` | 0,5 | Sinha (2007) §3.3 |
| Passo de integração FE | `DT = 1 / SINHA_FS_HZ` | 1/2560 s | convenção do projeto |
| Registro curto (órbitas/fase) | `T_SHORT` | 2 s | uso corrente |
| Registro longo (HOS) | `T_LONG` | 25 s | reservado à Sprint 02 |

A nota técnica
[`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md)
documenta esta cadeia em formato pronto para citação na seção de Métodos.

---

# `constants.py` — fonte única de verdade

A decisão arquitetural [D-002](DECISIONS.md) (2026-04-23) estabeleceu
[`constants.py`](../constants.py) como única origem de parâmetros do
caminho de replicação Sinha. Símbolos atualmente exportados:

- **Geometria do rotor** — `BEARING_1_NODE`, `BEARING_2_NODE`, `DISK_NODE`,
  `CRACK_NODE`, `PROBE_NODE` (consistentes com [`sinha_rotor.toml`](../sinha_rotor.toml)).
- **Desbalanceamento** — `UNB_MAG = Q_(2·10⁻⁴, "kg·m")`,
  `UNB_PHASE = Q_(4π/3, "rad")` — fase canônica que substituiu o valor
  inline `3π/4` antes presente no notebook 04 (registrado no *docstring*).
- **Velocidades de operação** — `SPEED_CRACK_0/1 = 650/750 rpm`,
  `SPEED_MIS_0/1 = 750/900 rpm`.
- **Trinca** — `CRACK_RATIO = 0.5`.

Todas as quantidades dimensionais usam `pint` (`Q_(...)`), com conversão
ao SI no ponto de uso (`.to("rad/s").m`). Esta convenção é repetida nos
guard-rails de [`CLAUDE.md`](../CLAUDE.md).

---

# Mapa de dependência entre notebooks

```
00_sinha_rotor.ipynb  ──  constrói geometria, calibra kxx → f₁ ≈ 27,50 Hz,
                          grava  sinha_rotor.toml
                                          │
                                          ▼
00a_modal_check.ipynb  ── asserção modal bloqueante (Sprint 00)
                                          │
                                          ▼
01a_sinha_rotor_modal.ipynb  ┐
01b_unbalance.ipynb          │   carregam sinha_rotor.toml via
02_sinha_unbalance_phase_crack.ipynb   rs.Rotor.load(...) e
03_sinha_crack_model_comparison.ipynb  importam constants.py
04_sinha_fault_analysis.ipynb (legacy) ┘
                                          │
                                          ▼
06_hos_validation.ipynb  ── testes A, B, C sobre signal_utils.py
07_hos_demo.ipynb        ── demonstração de QPC sintética (EN)
08_hos_qpc_demo_ptbr.ipynb ── tutorial QPC (PT-BR)
```

A propagação dos parâmetros (constants.py) e da geometria (sinha_rotor.toml)
fecha o ciclo de auditoria: nenhum *magic number* sobrevive em célula de
notebook sem rastreabilidade ao módulo central.

---

# O que falta para fechar §3.2 (Sprint 02 em curso)

Conforme [`PLAN.md`](PLAN.md) §1, a etapa em execução nesta data é a
**aquisição de registros longos persistidos em HDF5**, pré-condição para
todos os indicadores HOS quantitativos. Itens abertos:

- Estender [`constants.py`](../constants.py) com `DT_SIM`, `FS_SIM_NEWMARK`,
  `FS_ACQ_FE` e `SNR_DB` (referência à decisão D-005).
- Definir layout HDF5: um grupo por caso `(condition, speed_rpm)`,
  atributos `dt_sim`, `fs_out`, `aa_cutoff`, `snr_db`, `seed`, `git_sha`,
  `created_at`.
- Implementar `run_campaign.py` com a grade `{healthy, crack, misalignment}
  × {650, 750, 900} rpm`.
- Anexar testes de integração ao [`06_hos_validation.ipynb`](../06_hos_validation.ipynb)
  que releiam o primeiro caso e verifiquem contagem de segmentos e Δf.

A simulação determinística de resposta ao desbalanceamento (alvo §3.2
do plano) já é exercitada nos notebooks 01b / 02 / 03 sobre `T_SHORT`,
mas a verificação topológica completa da Fig. 9 de Sinha (órbita do
tipo *loop-containing-small-loop*) está endereçada apenas na Sprint 04.

---

# O que está fora deste estágio (não-metas declaradas)

Para proteger o cronograma de 5 semanas até a matriz de validação
(Sprint 07), [`sprints/README.md`](../sprints/README.md) e
[`DECISIONS.md`](DECISIONS.md) [D-003] excluem explicitamente do escopo
deste objetivo específico:

- Modelos de trinca `Flex Open` e `Flex Breathing` — apenas Mayes é
  exercitado em produção. Gasch permanece como comparação metodológica
  no notebook 03, sem entrar na matriz quantitativa.
- Extensão experimental RK4 — postergada para um próximo artigo.
- DoE paramétrico completo (profundidade × desalinhamento × velocidade ×
  amortecimento) — só é liberado se a matriz de validação Sprint 07
  obtiver pelo menos 8 de 10 reivindicações em estado *pass* ou
  *partial*.

A justificativa é metodológica: ampliar a campanha sobre um *pipeline*
não validado dilui a interpretação científica dos indicadores
bispectrais. A matriz das dez reivindicações falsificáveis de Sinha
(2007) está enumerada em [`sprints/README.md`](../sprints/README.md).

---

# Critério de aceitação consolidado (estado atual)

| Critério | Sprint | Estado em 2026-05-21 | Evidência |
|---|---|---|---|
| `|f₁ − 27,50| ≤ 0,05` Hz | 00 | atendido | [`00a_modal_check.ipynb`](../00a_modal_check.ipynb) célula A |
| Testes HOS A, B, C aprovados | 01 | atendido | [`06_hos_validation.ipynb`](../06_hos_validation.ipynb) |
| Δf = 1,25 Hz a `fs = 2560` | 01 | atendido por defaults | [`signal_utils.py`](../signal_utils.py) |
| `K(θ)` Mayes ↔ Sinha §5 (visual) | 00 / 04 | atendido (visual) em [`03_sinha_crack_model_comparison.ipynb`](../03_sinha_crack_model_comparison.ipynb) | — |
| Persistência em `results/campaign.h5` | 02 | **pendente** | — |
| `|ζ₁ − 0,003| ≤ 5·10⁻⁴` | 03 | **pendente** | — |
| Convergência de `NUM_MODES` ≤ 5 % | 03 | **pendente** | — |
| Órbita Sinha Fig. 9 reproduzida | 04 | **pendente** | — |
| B₁₃ presente / B₂₂ ausente (desalinh.) | 06 | **pendente** | — |
| Matriz de validação 10/10 reivindicações | 07 | **pendente** | — |

---

# Riscos ativos (registro atual)

Os riscos abaixo permanecem abertos em [`PLAN.md`](PLAN.md) §5 e devem
acompanhar a apresentação para que a banca avalie a maturidade do
pipeline na data de referência:

- **`run_misalignment` pode não reproduzir os pentes harmônicos densos
  de Sinha (Fig. 4) a 750/900 rpm.** Mitigação: *spike* nas duas
  primeiras jornadas da Sprint 06; falha sustentada é resultado
  científico legítimo e deve ser reportado, não escondido.
- **Integração de `T_LONG = 25 s` no laptop pode ser inviável.**
  Mitigação: medir um caso completo antes de comprometer a campanha de
  nove casos.
- **Truncamento `num_modes = 12` pode enviesar T₂₂₂.** Mitigação:
  tabela de convergência na Sprint 03 sobre o caso mais severo
  (desalinhamento a 900 rpm).
- **Floor de ruído `SNR_DB = 40` pode mascarar B₂₂.** Mitigação:
  varredura `SNR_DB ∈ {20, 30, 40, 60}` ainda na Sprint 01.

---

# Síntese — onde estamos na §3.2

O estágio §3.2 do planejamento global concluiu, até esta data:

1. **A construção e o congelamento de um modelo FE** rotor-mancal
   calibrado ao alvo experimental de Sinha (2007, §3), com infraestrutura
   de parâmetros unificada e contrato de geometria persistido.
2. **Um núcleo HOS auditado por testes falsificáveis**, com
   normalização Kim–Powers e estimadores compatíveis com a
   parametrização de Sinha (2007, §3.3).

Permanecem pendentes, em ordem de execução:

3. A **persistência de registros longos** (Sprint 02 — em curso).
4. A **calibração de amortecimento e convergência modal** (Sprint 03).
5. A **replicação FE-FE das Figs. 9 e 10** (Sprint 04).
6. A **validação quantitativa de HOS para trinca e desalinhamento**
   (Sprints 05 e 06) e a **matriz consolidada de dez reivindicações**
   (Sprint 07).

O estágio §3.2 só será declarado concluído quando os critérios da
Sprint 07 forem registrados em `results/validation_matrix.csv`.

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
*Journal of Vibration, Acoustics, Stress and Reliability in Design*, 106(1),
139–145.

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

Repositório: `01_Sinha_HOS_replication/` — versão consultada em
**2026-05-21**.
