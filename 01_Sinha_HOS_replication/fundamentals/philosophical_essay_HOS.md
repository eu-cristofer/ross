# Ecos do Invisível: A Epistemologia dos Sinais na Dinâmica de Rotores

> *"The exact phenomena for the generation of higher harmonics in case of misalignment is not yet known."* — Sinha (2007, p. 326)

## Abertura: O Diagnóstico sem Abrir a Máquina

Diagnosticar o estado interno de uma máquina rotativa em operação — sem desmontá-la, sem interromper sua função produtiva, sem sequer tocá-la — é, na sua essência, um exercício de epistemologia aplicada. A pergunta operacional ("há uma trinca?") é, no fundo, uma pergunta filosófica ("como podemos conhecer o oculto a partir do observável?"). Em rotodinâmica, a resposta não está na inspeção visual, mas na decodificação matemática dos sinais de vibração captados em sensores externos — proxies indiretos de uma realidade mecânica inacessível.

O desafio empírico que motiva esta investigação é estreito e bem definido: distinguir, exclusivamente a partir de sinais simulados em sensores, uma trinca transversal respirante (*breathing transverse crack*) de um desalinhamento paralelo de acoplamento (*parallel coupling misalignment*). Ambas as falhas geram, na resposta dinâmica do eixo, a componente 1X (frequência de rotação) acompanhada de 2X e harmônicos superiores (Sinha, 2007). É justamente essa coincidência espectral que historicamente mascara a causa-raiz de falhas catastróficas e que demanda uma lente analítica de maior resolução.

## O Paradoxo dos Sósias Espectrais

Trincas e desalinhamentos comportam-se, sob a Transformada de Fourier convencional, como *sósias espectrais*. A geração do 2X em um eixo trincado decorre da variação cíclica da rigidez à medida que a trinca abre e fecha sob a ação do peso próprio do rotor — fenômeno hoje canônico, atribuído por Sinha (2007) à formulação clássica de Mayes e Davies (1984) e revisado em profundidade por Wauer (1990) e Gasch (1993). Para o desalinhamento, a manifestação harmônica é igualmente conhecida, mas seu mecanismo gerador é menos consensual: Sinha (2007, p. 326) afirma textualmente que "the exact phenomena for the generation of higher harmonics in case of misalignment is not yet known", apoiando-se nas revisões de Ehrich (1992) e Dewell e Mitchell (1984) e nos modelos analíticos de Sekhar e Prabhu (1995) e Xu e Marangoni (1994).

A consequência epistemológica é direta. A Transformada de Fourier de segunda ordem — isto é, a Densidade Espectral de Potência (PSD) — opera sobre o conteúdo energético do sinal, ignorando a *fase* relativa entre as componentes harmônicas. Ela é capaz de sinalizar a *presença* de uma anomalia (há harmônicos onde só deveria haver o 1X), mas é estruturalmente incapaz de discriminar sua *origem mecânica*. Trinca e desalinhamento exibem o mesmo "vocabulário" espectral; a diferença reside na "gramática" — nas relações de fase entre os harmônicos —, e essa gramática é invisível à PSD.

## HOS como Lente Epistemológica

Os Espectros de Ordem Superior (HOS — *Higher Order Spectra*) movem a análise da segunda para a terceira e quarta ordem estatísticas, recuperando informação de fase. O biespectro é definido como a dupla Transformada de Fourier do momento de terceira ordem do sinal (Collis, White, & Hammond, 1998, *apud* Sinha, 2007); em termos operacionais:

$$B_{xxx}(f_l, f_m) = \mathbb{E}[X(f_l)\,X(f_m)\,X^{*}(f_l + f_m)], \quad l + m \leq N.$$

A interpretação física, conforme estabelecida pela tradição inaugurada por Fackrell et al. (1995a, 1995b) e sintetizada em Sinha (2007), é a de *acoplamento quadrático de fase*: o biespectro só é não-trivial em $(f_l, f_m)$ quando as três componentes $f_l$, $f_m$ e $f_l + f_m$ derivam de um mesmo processo não-linear subjacente, com fases mutuamente travadas. O triespectro estende o argumento à quarta ordem, capturando acoplamentos cúbicos:

$$T_{xxxx}(f_l, f_m, f_n) = \mathbb{E}[X(f_l)\,X(f_m)\,X(f_n)\,X^{*}(f_l + f_m + f_n)].$$

Se a metáfora da PSD é a do *prisma* (decomposição espectral em energias), a metáfora dos HOS é a do *interferômetro*: o que importa não é a intensidade isolada de cada frequência, mas a coerência relativa entre elas. Aquilo que era ruído de fase para a Fourier de segunda ordem torna-se assinatura para a HOS.

Empiricamente, Sinha (2007) demonstra que essa assinatura é categórica:

- **Trinca:** o biespectro exibe quatro picos — $B_{11}$, $B_{12}$ ($=B_{21}$) e $B_{22}$ — sendo este último ausente em baixas rotações e emergente em torno de 650 RPM, prominente a 750 RPM, em correlação com a transição do padrão de órbita "figura-oito" para "laço com sub-laço" próximo à metade da frequência natural (Sinha, 2007, Figs. 3 e 5). O triespectro é igualmente dependente da rotação, manifestando $T_{111}$, $T_{112}$, $T_{122}$ e $T_{222}$ (Fig. 7).
- **Desalinhamento:** cinco picos no biespectro — incluindo $B_{13}$ ($=B_{31}$) e ausência de $B_{22}$ — invariantes com a rotação no intervalo testado de 300–900 RPM (Sinha, 2007, Fig. 6). O triespectro, por sua vez, exibe apenas $T_{111}$ em todas as velocidades (Fig. 8).

A assimetria estrutural entre os dois padrões — variabilidade com rotação e a presença/ausência das diagonais $B_{22}$ e off-diagonais $B_{13}$ — constitui a "impressão digital" não-linear que a análise de Fourier convencional não consegue revelar.

## A Ressalva de Sinha, Lida com Precisão

A redação original deste ensaio atribuía a limitação de Sinha (2007) a uma deficiência de *infraestrutura computacional* ou de *modelos de Elementos Finitos disponíveis*. A leitura textual do §5 da fonte primária exige uma correção: a barreira que Sinha encontrou não foi computacional, mas *fenomenológica*. Nas palavras do próprio autor (Sinha, 2007, p. 332):

> *"Similar simulation for the misaligned shaft could not be done, as the force function due to the shaft misalignment is not well stood [understood]."*

A ressalva não é "faltou o método numérico"; é "faltou o conhecimento físico do termo de forçamento". Sinha conseguiu simular por Elementos Finitos a trinca respirante porque dispunha de um modelo cinemático canônico para o fenômeno — a função $(1 - \cos\theta)\,\Delta k / 2$ aplicada à equação do movimento, com $\theta$ medido a partir da posição fechada e $\Delta k$ a redução máxima de rigidez (Sinha, 2007, §5; cf. Sinha, Friswell, & Edwards, 2002). Para o desalinhamento, em 2007, não havia em sua mão um modelo igualmente bem fundamentado para a forçante de acoplamento, e o autor preferiu o silêncio técnico ao chute calibrado.

A consequência dessa ressalva é diretamente legível na arquitetura de figuras do artigo. Sinha (2007) apresenta, para a trinca, *quatro* tipos de evidência empilhada: espectros de amplitude experimentais (Fig. 2), órbitas (Fig. 3), biespectro experimental (Fig. 5), triespectro experimental (Fig. 7) e — coroando o conjunto — biespectro e triespectro derivados de Elementos Finitos (Fig. 10). Para o desalinhamento, o mesmo autor publica os equivalentes experimentais (Figs. 4, 6, 8) mas *interrompe* o argumento ali: não há Fig. 10-análoga, isto é, não há contrapartida FE das assinaturas $B_{13}$-presente-com-$B_{22}$-ausente-invariante-com-rotação (biespectro) nem da assinatura "apenas $T_{111}$" (triespectro). A lacuna não é interpretativa nem ilustrativa: é uma figura ausente, declarada como ausente, em uma posição definida do artigo.

**A contribuição que este programa entrega é, precisamente, essa figura ausente.** A meta operacional dos *Sprints* 04 e 06 é produzir, por simulação ROSS, o conjunto de assinaturas HOS de desalinhamento que reproduzem numericamente os achados experimentais de Sinha (2007, Figs. 6 e 8) — cinco picos no biespectro com $B_{13}$ ($=B_{31}$) presente e $B_{22}$ ausente, mantidos invariantes entre 750 e 900 RPM (Claim 6 da matriz de validação); um único componente $T_{111}$ no triespectro nos mesmos dois regimes (Claim 8). Esses são os Sinha-Fig-10-análogos do desalinhamento. A viabilidade dessa entrega apoia-se no fato de que, entre 2007 e 2026, a literatura amadureceu modelos de forçamento para desalinhamento de acoplamento flexível — implementados no ROSS via `run_misalignment` (modelo Xia et al., 2019) — que oferecem o *force function* cuja ausência Sinha declarou em §5. O ato científico aqui, portanto, não é replicação, mas *fechamento de lacuna documentada*: o predecessor delimitou explicitamente o que não pôde fazer, a infraestrutura subsequente passou a oferecer os meios, e a entrega tem coordenadas precisas (Figs. 6 e 8 de Sinha (2007), agora geradas por FE em vez de coletadas em bancada).

## A Disciplina do Sprint: Epistemologia Operacional

Há um parágrafo, aparentemente prosaico, que governa a arquitetura operacional deste programa de validação:

> *"Each sprint is a self-contained `.md` — purpose, prerequisites, work items, exit criteria. Hand any single file to an AI coding agent (or a student) and it should be executable without reading the others."* — `sprints/README.md`

À primeira vista, é um princípio de organização. Em sua substância, é a continuação metodológica do mesmo compromisso epistemológico que o HOS materializa no domínio dos sinais: **tornar o implícito explícito**. Onde o biespectro extrai do sinal a fase oculta que a PSD descarta, o *sprint* extrai da prática de pesquisa o contexto tácito que as descrições convencionais omitem — pré-condições, premissas, critérios de aceite. Três comprometimentos operam simultaneamente nesse parágrafo:

**Primeiro, encapsulamento contra a entropia tácita.** Conhecimento de pesquisa raramente falha por ausência de etapas; falha por etapas suposta e silenciosamente compartilhadas entre colaboradores. Ao exigir que cada *sprint* seja autocontido — propósito, pré-requisitos, itens de trabalho e critérios de saída em um único arquivo — o parágrafo institui que a inteligibilidade do passo não pode depender de informação que o leitor "deveria já saber". É a versão metodológica da exigência popperiana: o que não pode ser comunicado de forma operacionalizável e falsificável não conta como ciência.

**Segundo, simetria entre agente humano e agente artificial.** O parágrafo coloca, no mesmo plano, "um agente de codificação de IA" e "um estudante". A assimilação não é retórica: ela reconhece que um modelo de linguagem, ao iniciar uma tarefa, opera com o mesmo déficit de contexto de um colaborador recém-chegado — sem memória institucional, sem tacit knowledge, sem privilégio do que "todo mundo sabe". Um *sprint* que falha quando entregue a uma IA é também um *sprint* que falha quando entregue a um pesquisador externo, a um revisor, ou à versão futura do próprio autor (cuja memória curta tem custo bem documentado em arqueologia de software). A IA, neste regime, atua como *teste de carga* para a robustez documental.

**Terceiro, falsificabilidade incorporada via critérios de saída.** Cada *sprint* deste programa termina em um teste quantitativo associado a uma das dez afirmações falsificáveis derivadas de Sinha (2007) — a tabela "10 falsifiable claims" do `sprints/README.md`. O critério de saída não é "o código roda" nem "a figura parece razoável"; é "tal indicador escalar permanece dentro de tal banda quando reaplicado às mesmas condições". Esse desenho transpõe para o cotidiano da pesquisa a exigência que se faz ao biespectro: que a diferença entre "trinca" e "desalinhamento" se mostre não como impressão visual mas como teste estatístico — $B_{22}$ presente versus ausente, $T_{222}$ presente versus apenas $T_{111}$.

A homologia entre os dois domínios é, portanto, completa. O HOS é a epistemologia tornada algoritmo no sinal; o *sprint* é a epistemologia tornada protocolo na bancada. Ambos negam o privilégio do implícito. Ambos exigem que a verdade científica resida em um artefato que outro agente — humano ou artificial, presente ou futuro — possa, independentemente, re-executar.

## Síntese

O programa de validação aqui delineado tem duas faces que se reforçam. Na face matemática, ele toma o aparato de terceira e quarta ordens estatísticas dos HOS — biespectro e triespectro — e o aplica sistematicamente para extrair, dos sinais simulados, a informação de fase que a Fourier convencional descarta. Na face metodológica, ele organiza a execução em unidades modulares falsificáveis, cuja inteligibilidade independe do contexto humano específico, e cujo critério de sucesso é definido *ex ante* em termos quantitativos. Replicar Sinha (2007) é, neste regime, condição necessária mas não suficiente; a contribuição reside em fechar a lacuna fenomenológica que o próprio autor delimitou — a assinatura HOS do desalinhamento, simulada por Elementos Finitos com um modelo de forçamento que ele, em 2007, não possuía. O resultado almejado não é apenas um diagnóstico mais fino para falhas em rotores; é uma demonstração empírica de que comportamentos vibratórios não-lineares, e os processos científicos que os investigam, podem ambos ser submetidos à mesma disciplina: a de tornar o invisível auditável.

---

## Referências

Collis, W. B., White, P. R., & Hammond, J. K. (1998). Higher-order spectra: The bispectrum and trispectrum. *Mechanical Systems and Signal Processing*, *12*(3), 375–394. [As cited in Sinha (2007).]

Dewell, D. L., & Mitchell, L. D. (1984). Detection of a misaligned disk coupling using spectrum analysis. *Transactions of the ASME — Journal of Vibration, Acoustics, Stress, and Reliability in Design*, *106*(1), 9–16. [As cited in Sinha (2007).]

Ehrich, F. F. (Ed.). (1992). *Handbook of rotordynamics*. McGraw-Hill. [As cited in Sinha (2007).]

Fackrell, J. W. A., White, P. R., Hammond, J. K., Pinnington, R. J., & Parsons, T. A. (1995a). The interpretation of the bispectra of vibration signals — I. Theory. *Mechanical Systems and Signal Processing*, *9*(3), 257–266. [As cited in Sinha (2007).]

Fackrell, J. W. A., White, P. R., Hammond, J. K., Pinnington, R. J., & Parsons, T. A. (1995b). The interpretation of the bispectra of vibration signals — II. Experimental results and applications. *Mechanical Systems and Signal Processing*, *9*(3), 267–274. [As cited in Sinha (2007).]

Gasch, R. (1993). A survey of the dynamic behaviour of a simple rotating shaft with a transverse crack. *Journal of Sound and Vibration*, *160*(2), 313–332. [As cited in Sinha (2007).]

Mayes, I. W., & Davies, W. G. R. (1984). Analysis of the response of a multi-rotor-bearing system containing a transverse crack in a rotor. *Transactions of the ASME — Journal of Vibration, Acoustics, Stress, and Reliability in Design*, *106*, 139–145. [As cited in Sinha (2007).]

Sekhar, A. S., & Prabhu, B. S. (1995). Effects of coupling misalignment on vibrations of rotating machinery. *Journal of Sound and Vibration*, *185*, 655–671. [As cited in Sinha (2007).]

Sinha, J. K. (2007). Higher order spectra for crack and misalignment identification in the shaft of a rotating machine. *Structural Health Monitoring*, *6*(4), 325–334. https://doi.org/10.1177/1475921707082309

Sinha, J. K., Friswell, M. I., & Edwards, S. (2002). Simplified models for the location of cracks in beam structures using measured vibration data. *Journal of Sound and Vibration*, *251*(1), 13–38. [As cited in Sinha (2007).]

Wauer, J. (1990). On the dynamics of cracked rotors: A literature survey. *Applied Mechanics Reviews*, *43*(1), 13–17. [As cited in Sinha (2007).]

Xu, M., & Marangoni, R. D. (1994). Vibration analysis of a motor-flexible coupling-rotor system subjected to misalignment and unbalance, Parts I & II: Theoretical model and analysis. *Journal of Sound and Vibration*, *176*, 663–691. [As cited in Sinha (2007).]
