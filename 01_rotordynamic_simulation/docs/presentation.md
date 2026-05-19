---
marp: true
theme: default
paginate: true
header: "Diagnóstico de Falhas em Rotores via HOS — Replicação Numérica de Sinha (2007)"
footer: "Cristofer Antoni Souza Costa · POSMEC / UFU · 2026"
size: 16:9
style: |
  section { font-size: 24px; }
  section.lead h1 { font-size: 44px; }
  section.lead { text-align: center; }
  table { font-size: 20px; }
  pre { font-size: 18px; }
  h2 { color: #1f4e79; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Diagnóstico de Falhas em Máquinas Rotativas via Simulação Numérica e Espectros de Ordem Superior

**Replicação computacional de Sinha (2007) e extensão ao desalinhamento de acoplamento**

Cristofer Antoni Souza Costa
*Mestrado em Engenharia Mecânica — POSMEC / UFU*
Orientador: Prof. Dr. Aldemir Aparecido Cavallini Junior
Defesa prevista: fevereiro de 2026

---

## Como ler esta apresentação

Este arquivo é **Marp puro** (`marp: true` no frontmatter). Cada
separador `---` em linha isolada é uma quebra de slide; o cabeçalho /
rodapé / paginação são renderizados automaticamente pelo Marp.

**Renderizar / exportar:**

```bash
# Opção 1 — extensão Marp for VS Code (preview ao vivo + export)
code --install-extension marp-team.marp-vscode
# abra docs/presentation.md no VS Code → ícone Marp no canto superior direito

# Opção 2 — Marp CLI (gera PDF, HTML, PPTX)
npm install -g @marp-team/marp-cli
marp docs/presentation.md --pdf       # para a banca
marp docs/presentation.md --pptx      # para editar no PowerPoint
marp docs/presentation.md --html -w   # servidor com watch para preview
```

**Rota de leitura sugerida** (≈ 15 min para passada completa):

1. Slides 3–6 → **por que** esta pesquisa existe.
2. Slides 7–11 → **o que** será feito (metodologia + pipeline).
3. Slides 12–17 → **como** será feito (sprints + entregas).
4. Slides 18–22 → **onde estamos hoje** e o que vem a seguir.

**Convenções visuais usadas aqui:**

- ✅ → entregue e validado · 🟡 → em andamento · ⚠️ → risco / atenção · ❌ → fora de escopo

**Documentos complementares** (não duplicados nesta apresentação):

| Documento | Quando consultar |
|---|---|
| [`../README.md`](../README.md) | Visão geral do repositório + status por sprint |
| [`PLAN.md`](PLAN.md) | O que está sendo feito esta semana |
| [`DECISIONS.md`](DECISIONS.md) | Por que cada parâmetro / modelo foi escolhido |
| [`PAPER_NOTES.md`](PAPER_NOTES.md) | Mapeamento seção do artigo → evidência |
| [`../sprints/`](../sprints/) | Brief executável de cada sprint |

---

## 1. O contexto industrial

**Máquinas rotativas** — turbinas, compressores, bombas, geradores — são a
espinha dorsal das indústrias de energia, óleo e gás, aeroespacial e
manufatura.

**Custo de uma parada não planejada:** bilhões de dólares por ano,
globalmente.

**Duas falhas dominantes em eixos:**

| Falha | Mecanismo físico | Impacto industrial |
|---|---|---|
| **Trinca transversal** | Trinca por fadiga que "respira" durante a rotação, introduzindo variação não-linear de rigidez | Risco de ruptura catastrófica do eixo |
| **Desalinhamento de acoplamento** | Deslocamento angular ou paralelo entre eixos acoplados | Degradação de mancais e selos, vibração elevada |

Ambas geram **assinaturas dinâmicas não-lineares** — e é exatamente aí que
os **Espectros de Ordem Superior (HOS)** se tornam relevantes.

---

## 2. Por que Espectros de Ordem Superior (HOS)?

**Análise tradicional** — Densidade Espectral de Potência (PSD), uma
estatística de segunda ordem.

A PSD é **cega** para:

- **Acoplamento de fase** entre harmônicos (ex.: o acoplamento 1X–2X
  causado por uma trinca respirante)
- **Características não-Gaussianas** do sinal de vibração
- **Interações não-lineares** que distinguem trinca de desalinhamento

**HOS** — biespectro (3ª ordem) e triespectro (4ª ordem) — preservam
**informação de fase** e detectam não-linearidades quadráticas e cúbicas.

```
Abordagem tradicional:                Abordagem HOS:
Sinal → FFT → PSD                     Sinal → FFT → Biespectro / Triespectro
       (só amplitude)                        (amplitude + acoplamento de fase)
       NÃO distingue                         DISTINGUE assinaturas
       trinca vs. desalinhamento             não-lineares de cada falha
```

**Consequência prática.** HOS é teoricamente superior para distinguir
falhas que produzem conteúdo de frequência **parecido** mas padrões de
acoplamento não-linear **diferentes**.

---

## 3. O ponto de partida: Sinha (2007)

> Sinha, J. K. (2007). *Higher Order Spectra for Crack and Misalignment
> Identification in the Shaft of a Rotating Machine.*
> *Structural Health Monitoring* 6(4), 325–334.

**O que Sinha fez:**

- Aplicou biespectro e triespectro a sinais de vibração de uma bancada
  experimental com rotor flexível
- Mostrou que **trinca** e **desalinhamento** produzem **topologias HOS
  distintas** — em particular, a presença de `B22` e `T222` é um
  discriminador da trinca a 750 RPM
- Tentou reproduzir os resultados via simulação FE (§5, Fig. 10), com
  sucesso parcial para a trinca

**O que Sinha NÃO conseguiu fazer** *(§5, citação literal):*

> *"the force function due to the shaft misalignment is not well stood"*

Ou seja: **Sinha não conseguiu simular numericamente o desalinhamento.**
Suas conclusões sobre desalinhamento (Figs. 4, 6, 8) ficaram restritas ao
dado experimental.

---

## 4. A lacuna na literatura

| O que existe | O que falta |
|---|---|
| HOS aplicado a bancadas experimentais (Sinha 2007 e seguidores) | Estudo numérico sistemático com ferramentas abertas |
| ROSS — biblioteca FE de rotodinâmica em Python (Timbo et al. 2020) | Integração ROSS ↔ HOS |
| Modelos FEM de rotor com PSD / órbitas | Modelos FEM com **biespectro / triespectro** validados |
| Modelo Mayes-Davies de trinca respirante | Modelo FE de **desalinhamento** capaz de reproduzir as assinaturas HOS de Sinha |

**Limitações de bancadas experimentais:**

- Caras e demoradas
- Difícil isolar uma única falha com severidade conhecida
- Cobertura paramétrica limitada (uma bancada = uma configuração)
- Reprodutibilidade pobre entre laboratórios

**Proposta de valor:** simulação numérica controlada, totalmente
reprodutível, com varredura paramétrica sistemática.

---

## 5. A contribuição desta pesquisa

**Frase de elevador (uma sentença):**

> *Demonstramos que um pipeline FE totalmente aberto, baseado em ROSS,
> reproduz toda a assinatura biespectral e triespectral relatada
> experimentalmente por Sinha (2007) para uma trinca transversal
> respirante, e estendemos o resultado ao desalinhamento de acoplamento
> paralelo — caso que Sinha não conseguiu simular numericamente.*

**Três contribuições, em ordem de novidade:**

1. **Replicação numérica** das 10 afirmações falseáveis de Sinha (2007),
   com matriz de validação pontuada `pass` / `fail` / `partial`.
2. **Extensão ao desalinhamento** via modelo de acoplamento flexível de
   Xia et al. (2019) — a lacuna que Sinha declarou explicitamente.
3. **Pipeline aberto e reprodutível** (ROSS + `signal_utils.py` +
   `plot_utils.py`) que qualquer grupo de pesquisa pode reusar e
   estender.

---

## 6. A pergunta de pesquisa

> **Um pipeline de simulação numérica baseado em FE pode reproduzir, de
> forma quantitativa e falseável, as assinaturas biespectrais e
> triespectrais que Sinha (2007) observou experimentalmente para trinca
> transversal — e estender o resultado ao desalinhamento de acoplamento?**

**Critério de sucesso** *(definido a priori, não retroativamente):*

- ≥ 8 das 10 afirmações de Sinha pontuadas como `pass` ou `partial` na
  matriz de validação (Sprint 07).
- `B22 / T222` aparecendo no biespectro / triespectro da trinca a 750 RPM
  e **ausente** no desalinhamento.
- `B13` presente no desalinhamento e ausente / atenuado na trinca.
- Topologia do biespectro do desalinhamento **invariante com a rotação**
  (750 vs. 900 RPM).

Se < 8/10 → o pipeline NÃO está pronto. Vamos consertar antes de
publicar, em vez de empurrar um resultado frágil.

---

## 7. Metodologia — visão geral

**Stack:**

```
ROSS (FE rotodinâmica)
  └── geometria, mancais, disco, trinca (Mayes), desalinhamento (Xia 2019)
       └── integração temporal (Newmark-β, dt = 1/10 000 s)
            └── filtragem anti-alias (1 kHz) + downsample (1 kHz / 2 560 Hz)
                 └── injeção de ruído AWGN (SNR = 40 dB) — protocolo Sinha §5
                      └── HOS (signal_utils.py)
                           ├── biespectro (Kim-Powers 1979)
                           ├── triespectro (Collis et al. 1998)
                           └── 50 segmentos × 50 % overlap × Δf = 1.25 Hz (Sinha §3.3)
```

**Princípios de engenharia de software:**

- **`constants.py` é a fonte única de verdade** (Sprint 01, Padrão A).
- **`sinha_rotor.toml` é o contrato congelado de geometria** — gerado uma
  vez por `00_sinha_rotor.ipynb`, carregado por todos os notebooks de
  análise.
- **Pint em todo lugar** — `Q_(valor, "unidade")` para velocidades,
  desbalanceamento, offsets. Conversão só no ponto de uso.

---

## 8. O modelo: rotor de Sinha

**Geometria** *(calibrada para reproduzir a primeira frequência natural
experimental de Sinha):*

| Parâmetro | Valor | Origem |
|---|---|---|
| Tipo de elemento | Viga Euler–Bernoulli 2-nós, 4 DOF/nó | ROSS `ShaftElement` padrão |
| Frequência natural alvo `f₁` | **27,50 Hz** | Sinha §3, impulso experimental (Ewins) |
| Modelo de trinca | Mayes-Davies: `(1 − cos θ) Δk / 2` | Sinha §5 (correspondência exata) |
| Razão de profundidade da trinca | 0,5 | Sinha §5 |
| Amortecimento modal `ζ₁` | 0,3 % (proporcional à rigidez) | Sinha §5 |
| Desbalanceamento residual | `2 × 10⁻⁴ kg·m`, fase `4π/3 rad` | Canônico ([D-006](DECISIONS.md#d-006)) |

**Decisão crítica:** calibração contra o **resultado experimental de
Sinha (27,50 Hz)**, NÃO contra o FE próprio de Sinha (26,53 Hz). Ver
[D-001](DECISIONS.md#d-001).

**Nós-chave** *(congelados em `sinha_rotor.toml`):*

```
BEARING_1_NODE = 1     DISK_NODE = 6      CRACK_NODE = 7
BEARING_2_NODE = 11    PROBE_NODE = 10
```

---

## 9. O pipeline — fluxo de dois estágios

```
┌─────────────────────────────┐
│ 00_sinha_rotor.ipynb        │
│  • constrói geometria       │
│  • calibra kxx via brentq   │
│  • salva sinha_rotor.toml   │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ Notebooks de análise (carregam sinha_rotor.toml)        │
│                                                          │
│  01a → análise modal                                     │
│  01b → desbalanceamento (baseline)                       │
│  02  → trinca vs. desbalanceamento (varredura de fase)   │
│  03  → comparação de modelos de trinca                   │
│  04  → análise integrada de falhas (legado)              │
│  06  → validação HOS (testes unitários)                  │
│  07  → demonstração HOS                                  │
│  08  → tutorial QPC (português)                          │
│                                                          │
│  Próximos:                                               │
│  07' → replicação Fig. 10 (Sprint 04)                    │
│  08' → HOS trinca @ 650/750 RPM (Sprint 05)              │
│  09  → HOS desalinhamento @ 750/900 RPM (Sprint 06)      │
└─────────────────────────────────────────────────────────┘
```

**Por quê dois estágios?** Reprodutibilidade: a geometria é definida uma
única vez; alterações exigem regenerar o TOML e registrar em
[`DECISIONS.md`](DECISIONS.md).

---

## 10. As 10 afirmações falseáveis de Sinha

A matriz de validação (Sprint 07) pontua cada uma como
`pass` / `fail` / `partial`.

| # | Afirmação | Fonte Sinha | Sprint |
|---|---|---|---|
| 1 | `f₁` intacta ≈ 27,50 Hz; trincada totalmente aberta ≈ 26,25 Hz | §3, §5 | 00 |
| 2 | Espectro de amplitude trincado mostra 1X + 2X + harmônicos superiores | Fig. 2 | 05 |
| 3 | Órbitas trincadas: figura-8 → laço-com-laço-pequeno | Fig. 3 | 05 |
| 4 | Espectro do desalinhamento mostra "pentes" harmônicos densos | Fig. 4 | 06 |
| 5 | Biespectro da trinca: `B22` emerge a 650, prominente a 750 (depende de velocidade) | Fig. 5 | 05 |
| 6 | Biespectro do desalinhamento: `B13` presente, `B22` ausente, invariante com velocidade | Fig. 6 | 06 |
| 7 | Triespectro da trinca depende da velocidade; `T222` aparece a 750 | Fig. 7 | 05 |
| 8 | Triespectro do desalinhamento: apenas `T111` em ambas as velocidades | Fig. 8 | 06 |
| 9 | Rotor saudável: `|B|, |T| < 0,3` (piso de ruído) | §4 | 02, 05, 06 |
| 10 | FE próprio de Sinha (Fig. 10) reproduzível numericamente | §5 | 04 |

---

## 11. Por que HOS distingue trinca de desalinhamento — intuição

**Trinca respirante.** A rigidez varia como `Δk · (1 − cos θ) / 2` ao
longo de uma rotação. Isso introduz uma **não-linearidade quadrática** na
resposta — gera acoplamento de fase entre `f` e `2f` (manifesta-se em
`B22`).

**Desalinhamento paralelo.** A força de acoplamento é fundamentalmente
**harmônica** — gera componentes em `1X, 2X, 3X, …` com **fases
estáveis** mas **sem acoplamento quadrático** entre `f` e `2f`.

**Consequência espectral:**

```
                Biespectro      Triespectro     Velocidade
                ─────────────   ─────────────   ──────────────
Saudável        nada (< 0,3)    nada (< 0,3)    —
Trinca @ 750    B11, B22 fortes T111, T222      DEPENDE
Desalinh. @750  B11, B13        somente T111    INVARIANTE
```

**`B22` e `T222` são os "fingerprints" da trinca.** **`B13` é o
"fingerprint" do desalinhamento.** É essa **dissimilaridade topológica** —
não a amplitude — que torna o HOS um diagnóstico viável.

---

## 12. Plano em 8 sprints

| # | Sprint | Esforço | Status | Entrega |
|---|---|---|---|---|
| 00 | Validação modal contra Sinha §3 / §5 | ½ dia | **✅ feito** | `00a_modal_check.ipynb` |
| 01 | Biblioteca HOS + testes sintéticos | 5 dias | **✅ feito** | `signal_utils.py`, `plot_utils.py`, `06_hos_validation.ipynb` |
| 02 | Aquisição casada com Sinha + registros longos | 3 dias | **🟡 em andamento** | `run_campaign.py`, `results/campaign.h5` |
| 03 | Calibração de amortecimento `ζ₁ = 0,3 %` + convergência modal | 2 dias | aguardando | `sinha_rotor.toml` reamortecido |
| 04 | Replicação FE-para-FE das Figs. 9 e 10 de Sinha | 3–5 dias | aguardando | `07_sinha_fig10_replication.ipynb` |
| 05 | HOS da trinca a 650 / 750 RPM (Figs. 2, 3, 5, 7) | 1 semana | aguardando | `08_crack_hos_650_750.ipynb` |
| 06 | HOS do desalinhamento a 750 / 900 RPM (Figs. 4, 6, 8) | 1 semana | aguardando | `09_misalignment_hos_750_900.ipynb` |
| 07 | Matriz de validação + Métodos | 3–5 dias | aguardando | `results/validation_matrix.csv`, `01_article/03_methods_draft.md` |

**Total nominal:** ≈ 5 semanas de trabalho efetivo.

---

## 13. Grafo de dependências entre sprints

```
00 ── 01 ── 02 ── 03 ── 04
                  │     │
                  ├──> 05 ─┐
                  └──> 06 ─┴──> 07
```

- Sprints **00 → 03** são lineares — cada um bloqueia o seguinte.
- Sprint **04** (replicação Fig. 10) roda em paralelo com 05 após 03.
- Sprints **05 e 06** rodam em paralelo (grupos HDF5 independentes).
- Sprint **07** consome o "Execution Log" de todos os anteriores.

**Por que esta ordem?** A biblioteca HOS (01) precisa estar correta
**antes** de qualquer dado simulado passar por ela — caso contrário, um
estimador quebrado dá resultados que parecem certos mas escondem bugs
sistemáticos (especialmente em normalização de bicoerência).

---

## 14. O contributo metodológico do Sprint 02

**O problema.** Os registros atuais são 2 s @ 2 560 Hz = 5 120 amostras.
O estimador de Sinha precisa de:

- 50 segmentos × 50 % overlap × Δf = 1,25 Hz
- → `Nfft = 2048` por segmento → ≈ 52 000 amostras → ≈ 20 s de registro

**Os dados atuais são ≈ 10× curtos demais.**

**A solução** *(Sinha §5, verbatim):*

```
Newmark-β @ dt = 1/10 000 s   ←  integração FE muito fina
       │
       ▼
Filtro passa-baixa @ 1 kHz   ←  anti-alias (Butterworth ordem 8)
       │
       ▼
Downsample para 1 kHz ou 2 560 Hz   ←  taxa de aquisição alvo
       │
       ▼
Injeção de AWGN @ SNR = 40 dB   ←  ruído controlado
       │
       ▼
HOS → biespectro / triespectro
```

Esse protocolo elimina a integração numérica como variável de confusão na
hora de pontuar `B22` / `T222`.

---

## 15. Riscos e mitigações

| Risco | Probab. | Impacto | Mitigação |
|---|---|---|---|
| `run_misalignment` do ROSS não produz pentes harmônicos densos a 750 / 900 RPM | média | **alta** (mata o contributo "novel") | *Spike* logo no início do Sprint 06 — primeiros 2 dias. Plano B: documentar a falha como achado metodológico. |
| Registros longos do Sprint 02 fazem a integração ficar lenta demais no laptop | média | média | Perfilar uma corrida `T_LONG` antes de comitar com as 9 casas. Se > 30 min/caso → mover campanha para workstation. |
| Truncamento `num_modes=12` enviesa amplitudes de `T222` | média | média | Sprint 03: tabela de convergência sobre `{8, 12, 16, 20}` no pior caso (desalinhamento @ 900 rpm). |
| Ruído de `SNR = 40 dB` afoga `B22` em baixas amplitudes | baixa | média | Testar Sprint 01 em `SNR ∈ {20, 30, 40, 60}` para mapear o piso antes do Sprint 05. |
| Matriz de validação < 8/10 → DoE adiado → tese perde perna "estudo paramétrico" | baixa-média | **alta** | Plano B: pivotar capítulo da tese para "profundidade da validação" usando a matriz de 10 afirmações como manchete. |

**Princípio.** Não maquiar um pipeline não-validado com mais corridas. A
contribuição publicável é um **pipeline confiável**, não um DoE
apressado.

---

## 16. Não-objetivos (proteção do escopo de 5 semanas)

Itens **explicitamente fora** desta dissertação / artigo:

- ❌ Modelos `Flex Open` / `Flex Breathing` de trinca. **Apenas Mayes**
  (que corresponde exatamente a Sinha §5). Ver [D-003](DECISIONS.md#d-003).
- ❌ Extensão experimental via RK4 (`01_article/04_rk4_working_plan.md`).
  É material para o **próximo artigo**.
- ❌ DoE completo (varredura de profundidade × desalinhamento × velocidade
  × amortecimento). Só liberado **depois** que a matriz de validação
  pontuar ≥ 8/10. Ver [D-007](DECISIONS.md#d-007).
- ❌ Comparação com EMD / wavelet / ML. A pergunta de pesquisa é sobre
  HOS especificamente.

**Por quê?** Cada item descartado seria uma contribuição menor sozinho,
mas todos juntos estouram o cronograma e diluem a mensagem central.

---

## 17. Cronograma macro

```
2026
├── Jan  ─ Sprints 00, 01  ✅
├── Fev  ─ ─ DEFESA DA DISSERTAÇÃO ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
├── Mar  ─ Sprint 02 (em andamento)
├── Abr  ─ Sprint 03 + início Sprint 04
├── Mai  ─ Sprint 04 + início Sprints 05 / 06 (paralelo)
├── Jun  ─ Sprints 05 / 06 (paralelo)
├── Jul  ─ Sprint 07 — matriz de validação + Métodos
├── Ago  ─ Redação do artigo (rascunho 1)
├── Set  ─ Submissão ao periódico (MSSP / JSV / SHM)
```

> ⚠️ **Atenção:** o cronograma acima precisa ser revisitado. A defesa em
> fevereiro de 2026 é o marco rígido; com o Sprint 02 ainda em andamento
> em maio, a sequência 03 → 07 precisa caber em ≈ 9 meses, o que é
> factível mas demanda disciplina de escopo.

---

## 18. Onde estamos hoje (2026-05-19)

**✅ Concluído.**

- Sprint 00 — calibração modal contra `27,50 Hz` validada.
- Sprint 01 — biblioteca HOS com testes positivos e negativos passando.
- Demos didáticas em inglês (`07_hos_demo.ipynb`) e português
  (`08_hos_qpc_demo_ptbr.ipynb`).
- Documentação de gestão: `README.md`, `docs/DECISIONS.md`,
  `docs/PLAN.md`, `docs/PAPER_NOTES.md`, este `presentation.md`.

**🟡 Em andamento.**

- Sprint 02 — `run_campaign.py` ainda não escrito; constantes
  `DT_SIM`, `FS_SIM_NEWMARK`, `FS_ACQ_FE`, `SNR_DB` pendentes em
  `constants.py`.

**⚠️ Dívida técnica conhecida** *(de `code_review.md`):*

- Notebook `04` ainda sobrescreve `CRACK_NODE`, `CRACK_RATIO`,
  `FREQ_RANGE`, `MIS_X/Y` inline.
- Helpers compartilhados ainda parcialmente extraídos para
  `sinha_helpers.py`.

Detalhes vivos em [`docs/PLAN.md`](PLAN.md).

---

## 19. Entregas finais previstas

**Tese (POSMEC / UFU, fevereiro de 2026):**

- Capítulo de Métodos rastreável até constantes / decisões / sprints
- Matriz de validação como tabela headline
- Apêndice com decisões arquiteturais ([`DECISIONS.md`](DECISIONS.md))

**Artigo de periódico (submissão ≈ 2 meses após defesa):**

- Alvos: *Mechanical Systems and Signal Processing* (preferencial),
  *Journal of Sound and Vibration*, *Structural Health Monitoring*
- 8–12 páginas
- Foco no **resultado novel**: HOS do desalinhamento via FE — a lacuna
  declarada por Sinha (2007)

**Artefato aberto:**

- Repositório público com pipeline reprodutível ponta a ponta
- DOI via Zenodo para o snapshot da submissão
- README com instruções de reprodução em uma única sessão de trabalho

---

## 20. Por que vale a pena ler esta pesquisa

Para um **engenheiro de manutenção**: um diagnóstico que distingue trinca
de desalinhamento **antes** que a falha catastrófica aconteça, sem
precisar de uma bancada experimental.

Para um **pesquisador de rotodinâmica**: um pipeline FE-HOS aberto que
pode ser estendido para novos tipos de falha, novas geometrias, novos
acoplamentos.

Para um **revisor de periódico**: uma matriz de 10 afirmações falseáveis,
cada uma com um critério numérico pré-definido e um resultado `pass` /
`fail` / `partial` — o oposto de "olhei o gráfico e ficou bonito".

Para a **comunidade ROSS**: o primeiro estudo HOS construído inteiramente
sobre a biblioteca, servindo como caso de validação para futuros
trabalhos.

---

## 21. Próximos passos imediatos

**Próximas duas semanas:**

1. Adicionar constantes de aquisição longa em `constants.py` (Sprint 02).
2. Implementar `run_campaign.py` com grid `{healthy, crack, misalignment}
   × {650, 750, 900}` rpm.
3. Persistir os 9 casos em `results/campaign.h5` com metadados completos
   (`git_sha`, `seed`, `dt_sim`, `fs_out`, `aa_cutoff`, `snr_db`).
4. Encerrar os P1 abertos em `code_review.md` enquanto o notebook `04`
   ainda está aberto.
5. Atualizar [`docs/PLAN.md`](PLAN.md) ao fim de cada item.

**Próximo mês:**

- Sprint 03 — calibrar amortecimento e fazer a tabela de convergência
  modal.
- Iniciar Sprint 04 (replicação Fig. 10) — primeiro alvo de validação
  FE-para-FE.

---

## 22. Referências essenciais

**Paper de referência:**

> Sinha, J. K. (2007). Higher Order Spectra for Crack and Misalignment
> Identification in the Shaft of a Rotating Machine.
> *Structural Health Monitoring* 6(4), 325–334.

**Fundamentos de HOS:**

> Kim, Y. C., & Powers, E. J. (1979). Digital Bispectral Analysis and
> Its Applications to Nonlinear Wave Interactions. *IEEE Trans. Plasma
> Sci.* 7(2), 120–131. — *Convenção de normalização.*

> Collis, W. B., White, P. R., & Hammond, J. K. (1998). Higher-order
> spectra: the bispectrum and trispectrum. *MSSP* 12(3), 375–394.
> — *Implementação de referência.*

**Ferramenta computacional:**

> Timbó, R. et al. (2020). ROSS — Rotordynamic Open Source Software.
> *Journal of Open Source Software*, 5(48), 2120.

**Modelo de desalinhamento (extensão novel):**

> Xia, Y. et al. (2019). Vibration characteristics of a rotor-bearing
> system with shaft misalignment. *Proc. IMechE Part C* 233(10).

Lista completa de citações coletadas e pendentes em
[`docs/PAPER_NOTES.md`](PAPER_NOTES.md) §7.

---

## Obrigado

**Cristofer Antoni Souza Costa**
*Mestrando — POSMEC / Universidade Federal de Uberlândia*
Orientador: Prof. Dr. Aldemir Aparecido Cavallini Junior

**Repositório:** `ross/01_rotordynamic_simulation/`
**Documentos vivos:**

- [`README.md`](../README.md) — visão geral + status
- [`docs/PLAN.md`](PLAN.md) — o que está sendo feito agora
- [`docs/DECISIONS.md`](DECISIONS.md) — por que cada coisa é como é
- [`docs/PAPER_NOTES.md`](PAPER_NOTES.md) — caminho até o artigo
- [`sprints/`](../sprints/) — briefs executáveis sprint a sprint

*Perguntas, críticas e sugestões são bem-vindas.*
