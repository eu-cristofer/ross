# A Matemática dos Espectros de Ordem Superior: Tutorial Anotado

> *Tutorial-companheiro do ensaio* [`philosophical_essay_HOS.md`](philosophical_essay_HOS.md) *e do caderno computacional* [`HOS_math_tutorial.ipynb`](HOS_math_tutorial.ipynb)*. Aqui se constrói, com fundamentação textual rigorosa, a ponte matemática entre o tratamento determinístico do espectro feito em Oppenheim, Willsky e Nawab (1997) e as definições operacionais de biespectro e triespectro apresentadas em* Sinha (2007, §2).

## 1. O que a §2 de Sinha (2007) efetivamente afirma

O artigo de Sinha (2007) dedica pouco mais de uma página ao aparato matemático que sustenta todo o seu argumento experimental. A seção 2.1 introduz o biespectro pela diferença em relação à densidade espectral de potência (PSD): "The conventional power spectrum density (PSD) provides information on the second-order properties (i.e., energy) of a signal whereas the bi-spectrum can provide information on the signal's third-order properties" (Sinha, 2007, p. 327). A formalização ocorre em três equações:

$$
S_{xx}(f_k) = \mathbb{E}\!\left[X(f_k)\,X^{*}(f_k)\right], \quad k = 1, 2, 3, \ldots, N \tag{Sinha Eq. 1}
$$

$$
B_{xxx}(f_l, f_m) = \mathbb{E}\!\left[X(f_l)\,X(f_m)\,X^{*}(f_l + f_m)\right], \quad l + m \leq N \tag{Sinha Eq. 2}
$$

$$
T_{xxxx}(f_l, f_m, f_n) = \mathbb{E}\!\left[X(f_l)\,X(f_m)\,X(f_n)\,X^{*}(f_l + f_m + f_n)\right], \quad l + m + n \leq N \tag{Sinha Eq. 3}
$$

Sinha (2007, p. 327) caracteriza o biespectro como "the double Fourier transformation of the third-order moment of a time signal" e o triespectro como "the triple Fourier transformation of the fourth-order moment of a time signal". A interpretação física do biespectro é dada como medida do "amount of coupling between the frequencies at $f_l$, $f_m$, and $f_l + f_m$", e nomeada como *quadratic phase coupling* (acoplamento quadrático de fase). O artigo fecha a seção com a afirmação programática de que os HOS "are the non-linear estimators".

Quatro elementos dessa formalização não são explicados no artigo e exigem fundamentação: (i) por que $X(f_k)$ tem significado bem definido para sinais de duração finita amostrados; (ii) o que o operador $\mathbb{E}[\cdot]$ representa, e por que aparece; (iii) por que o produto triplo $X(f_l)\,X(f_m)\,X^{*}(f_l + f_m)$ detecta acoplamento de fase; (iv) por que a extensão de quarta ordem captura não-linearidades cúbicas. As seções seguintes constroem cada um desses passos a partir de material anterior ao próprio artigo.

## 2. A Fundação Determinística — Oppenheim, Willsky e Nawab (1997)

### 2.1 A Transformada de Fourier de Tempo Discreto

Oppenheim, Willsky e Nawab (1997, p. 361) definem o par DTFT para uma sequência aperiódica $x[n]$ pelas equações de análise e de síntese:

$$
X(e^{j\omega}) = \sum_{n=-\infty}^{+\infty} x[n]\,e^{-j\omega n} \tag{Oppenheim Eq. 5.9}
$$

$$
x[n] = \frac{1}{2\pi}\int_{2\pi} X(e^{j\omega})\,e^{j\omega n}\,d\omega \tag{Oppenheim Eq. 5.8}
$$

A função $X(e^{j\omega})$ é o *espectro* de $x[n]$ e expressa "how $x[n]$ is composed of complex exponentials" (Oppenheim et al., 1997, p. 361). Esta é a base determinística do conceito de "DFT" usado em Sinha (2007, p. 327, Eq. 1): para sinais de duração finita amostrados a frequência $f_s$, o objeto computado é $X(f_k)$ avaliado em frequências discretas $f_k = k f_s/N$. Embora Oppenheim et al. (1997) não dediquem um capítulo separado à DFT computacional propriamente dita, o objeto resulta diretamente da DTFT aplicada à sequência finita estendida por periodicidade (Oppenheim et al., 1997, Cap. 5).

### 2.2 Magnitude e Fase como Informação Independente

Em Oppenheim, Willsky e Nawab (1997, §6.1, p. 423), a transformada admite a representação magnitude-fase:

$$
X(e^{j\omega}) = \bigl|X(e^{j\omega})\bigr|\,e^{j\,\angle X(e^{j\omega})} \tag{Oppenheim Eq. 6.2}
$$

O ponto pedagogicamente crucial é que os autores afirmam, com força, que magnitude e fase carregam **informações distintas e ambas substantivas**. A passagem é citada na íntegra (Oppenheim et al., 1997, p. 424):

> "The phase angle $\angle X(j\omega)$, on the other hand, does not affect the amplitudes of the individual frequency components, but instead provides us with information concerning the relative phases of these exponentials. The phase relationships captured by $\angle X(j\omega)$ have a significant effect on the nature of the signal $x(t)$ and thus typically contain a substantial amount of information about the signal. In particular, depending upon what this phase function is, we can obtain very different-looking signals, even if the magnitude function remains unchanged."

A Figura 6.1 do mesmo texto demonstra que três cossenoides com magnitudes idênticas e fases distintas produzem formas de onda visualmente irreconhecíveis umas das outras (Oppenheim et al., 1997, p. 425). Já se anuncia, portanto, sem nenhum apelo a conceitos estatísticos, que **descartar a fase apaga informação substantiva**.

### 2.3 Energia Espectral — o Análogo Determinístico

A relação de Parseval para o DTFT é dada em Oppenheim, Willsky e Nawab (1997, p. 380):

$$
\sum_{n=-\infty}^{+\infty} \bigl|x[n]\bigr|^{2} = \frac{1}{2\pi}\int_{2\pi} \bigl|X(e^{j\omega})\bigr|^{2}\,d\omega \tag{Oppenheim Eq. 5.47}
$$

O lado esquerdo é a energia total do sinal; o lado direito identifica $\bigl|X(e^{j\omega})\bigr|^{2}$ como uma *densidade* de energia ao longo da frequência. Os mesmos autores se referem a esse objeto, em contexto contínuo análogo, como *energy-density spectrum* (Oppenheim et al., 1997, p. 424). Crucialmente, este objeto é estritamente **determinístico** — depende apenas de $x[n]$ — e descarta a fase, pois $\bigl|X(e^{j\omega})\bigr|^{2} = X(e^{j\omega})\,X^{*}(e^{j\omega})$.

## 3. O Salto Estatístico que Oppenheim et al. (1997) Não Atravessam

A obra de Oppenheim, Willsky e Nawab (1997) trata sinais como sequências numéricas determinísticas: seu sumário (1997, pp. vii–xv) não contém capítulo sobre processos estocásticos, esperança, momentos estatísticos, autocorrelação no sentido aleatório ou densidade espectral *de potência* no sentido estatístico. O único análogo é o "energy-density spectrum" puramente determinístico do §6.1.

Sinha (2007, p. 327), ao escrever $S_{xx}(f_k) = \mathbb{E}[X(f_k)\,X^{*}(f_k)]$, introduz o operador $\mathbb{E}[\cdot]$ (esperança estatística) — e com ele move o problema do domínio determinístico para o estocástico. Tal salto pressupõe que $x[n]$ é uma realização de um processo aleatório estacionário, e que múltiplas realizações (ou múltiplos segmentos do mesmo sinal, sob hipótese de ergodicidade) podem ser promediadas para estimar o objeto teórico. A operacionalização concreta dessa esperança no artigo é descrita explicitamente (Sinha, 2007, p. 329): "50 segments using 50% overlap in the time data with the frequency resolution of 1.25 Hz were used for the averaging of the computed HOS". O fundamento teórico é creditado por Sinha às referências Collis, White e Hammond (1998) e Fackrell et al. (1995a, 1995b), que não foram diretamente consultados no presente corpus.

Conceitualmente, portanto, há **duas grandezas paralelas** com nomes parecidos:

| Grandeza | Fonte | Operação | Domínio |
|---|---|---|---|
| Espectro de densidade de energia $\bigl\|X(e^{j\omega})\bigr\|^{2}$ | Oppenheim et al. (1997, §6.1) | Determinística sobre $x[n]$ específica | Sinais aperiódicos de energia finita |
| Densidade espectral de potência $S_{xx}(f_k) = \mathbb{E}\!\left[X(f_k)X^{*}(f_k)\right]$ | Sinha (2007, Eq. 1) apoiado em literatura estatística externa | Esperança sobre realizações do processo | Processos aleatórios estacionários |

Ambas refletem informação de magnitude e descartam fase relativa entre componentes. A diferença é que a primeira é exata para uma sequência específica e a segunda estima uma propriedade do processo subjacente.

## 4. Momentos de Ordem Superior na Frequência

### 4.1 Motivação não-linear

Sinha (2007, p. 327) afirma diretamente a motivação para ultrapassar a segunda ordem estatística:

> "The concept of correlating different harmonic components (both amplitudes and phases) in the HOS clearly indicates that they are the non-linear estimators. It is because the non-linear behavior in the structural dynamics generates several harmonics of the exciting frequencies."

A leitura cuidadosa exige uma observação técnica que o artigo não desenvolve, mas que é mencionada de passagem: a PSD, por construção, é cega à fase relativa entre componentes de frequência distintas. Um processo cujo conteúdo de magnitude espectral é fixo mas cuja relação de fase entre componentes harmônicas varia entre realizações terá, em esperança, exatamente a mesma PSD. Para distinguir tais processos é necessário um estimador que opere sobre triplas ou quádruplas de frequências simultaneamente, mantendo informação de fase.

### 4.2 O biespectro como produto triádico com fase preservada

A definição $B_{xxx}(f_l, f_m) = \mathbb{E}\!\left[X(f_l)\,X(f_m)\,X^{*}(f_l + f_m)\right]$ (Sinha, 2007, Eq. 2) admite uma leitura estrutural transparente quando se parte da representação magnitude-fase de Oppenheim et al. (1997, Eq. 6.2). Escrevendo $X(f_k) = \bigl|X(f_k)\bigr|\,e^{j\varphi(f_k)}$, o produto interno à esperança fica:

$$
X(f_l)\,X(f_m)\,X^{*}(f_l + f_m) = \bigl|X(f_l)\bigr|\,\bigl|X(f_m)\bigr|\,\bigl|X(f_l + f_m)\bigr|\;e^{\,j\bigl[\varphi(f_l) + \varphi(f_m) - \varphi(f_l + f_m)\bigr]}.
$$

A fase total é portanto $\varphi(f_l) + \varphi(f_m) - \varphi(f_l + f_m)$ — exatamente a *diferença* entre (a) a soma das fases de duas componentes e (b) a fase da componente cuja frequência é a soma. Esta diferença é o objeto central. Dois cenários extremos esclarecem o comportamento da esperança:

- **Componentes independentes.** Se $\varphi(f_l + f_m)$ é estatisticamente independente das fases $\varphi(f_l)$ e $\varphi(f_m)$ — i.e., as três componentes provêm de mecanismos físicos não relacionados —, então a fase total $\varphi(f_l) + \varphi(f_m) - \varphi(f_l + f_m)$ se distribui uniformemente sobre $[0, 2\pi)$ entre realizações, e a esperança do exponencial complexo $e^{j(\cdot)}$ tende a zero. Em consequência, $B_{xxx}(f_l, f_m) \to 0$.
- **Componentes acopladas.** Se as três componentes derivam de um mesmo mecanismo não-linear que acopla $f_l$ e $f_m$ para gerar $f_l + f_m$ — i.e., a fase em $f_l + f_m$ é uma função determinística das fases em $f_l$ e $f_m$ —, então a fase total é constante (ou ao menos não-uniformemente distribuída), e a esperança não se anula. Em consequência, $\bigl|B_{xxx}(f_l, f_m)\bigr| > 0$.

Esta é a definição operacional de **acoplamento quadrático de fase**, reportada textualmente em Sinha (2007, p. 327): "The bi-spectrum is complex and interpreted as measuring the amount of coupling between the frequencies at $f_l$, $f_m$, and $f_l + f_m$, and is described by 'quadratic phase coupling'."

O biespectro, portanto, mede uma propriedade de coerência triádica entre frequências — uma propriedade que a PSD, pela própria construção como média de $\bigl|X(f_k)\bigr|^{2}$, descarta a priori (a aviso de Oppenheim et al., 1997, p. 424, sobre a importância da fase encontra aqui aplicação operacional).

### 4.3 O triespectro e os acoplamentos cúbicos

A extensão à quarta ordem segue a mesma lógica (Sinha, 2007, Eq. 3): o produto quádruplo $X(f_l)\,X(f_m)\,X(f_n)\,X^{*}(f_l + f_m + f_n)$ tem fase $\varphi(f_l) + \varphi(f_m) + \varphi(f_n) - \varphi(f_l + f_m + f_n)$ e é, em esperança, não-zero apenas quando essa diferença não se aleatoriza entre realizações. Triadas $T_{111}$, $T_{112}$, $T_{122}$, $T_{222}$ — notação introduzida em Sinha (2007, Fig. 7) — sondam famílias específicas de acoplamento cúbico (envolvendo três componentes geradoras e uma componente de soma).

## 5. A Discriminação Trinca-Desalinhamento como Geometria de Fase

A motivação física desenvolvida em Sinha (2007, §1) é que trinca respirante e desalinhamento de acoplamento paralelo produzem *o mesmo* conjunto de harmônicos de 1X — conteúdo de magnitude similar na PSD — mas via mecanismos não-lineares estruturalmente diferentes. A geometria do acoplamento de fase resultante difere entre as duas falhas, e o biespectro/triespectro a expõe (Sinha, 2007, §4):

- **Trinca:** quatro picos no biespectro — $B_{11}$, $B_{12}$ ($=B_{21}$) e $B_{22}$ —, este último ausente em baixas rotações e emergente em 650 RPM, proeminente em 750 RPM, em coincidência com a transição do padrão de órbita "figura-oito" para "laço com sub-laço" próximo à metade da frequência natural (Sinha, 2007, Figs. 3 e 5). Triespectro dependente da rotação, com $T_{111}$, $T_{112}$, $T_{122}$, $T_{222}$ (Fig. 7).
- **Desalinhamento:** cinco picos no biespectro com $B_{13}$ ($=B_{31}$) presente e $B_{22}$ ausente, invariantes com a rotação entre 300 e 900 RPM (Sinha, 2007, Fig. 6). Triespectro com apenas $T_{111}$ (Fig. 8).

A diferença é diagnóstica precisamente porque é uma diferença de *fase* — i.e., de quais triadas de frequências têm acoplamento sustentado entre realizações — e não de magnitude. O alerta de Oppenheim, Willsky e Nawab (1997, p. 424) de que "the phase relationships [...] have a significant effect on the nature of the signal" encontra, aqui, sua aplicação canônica à engenharia de manutenção preditiva.

## 6. Limites de cada lado da ponte

O leitor deve sustentar clareza sobre o que cada referência cobre e o que não cobre, especialmente porque o argumento estendido neste tutorial é uma síntese entre dois textos com escopos disjuntos.

Oppenheim, Willsky e Nawab (1997) fundamentam a representação espectral determinística — DTFT, magnitude/fase, energia, multiplicação/convolução, amostragem, sistemas LTI. O sumário (1997, pp. vii–xv) e a estrutura dos capítulos não tratam de processos estocásticos, PSD estatística, momentos de ordem superior nem HOS. Tais tópicos são tratados em outros volumes da série Prentice Hall em que Oppenheim atua como editor — em particular Nikias e Petropulu (citados como volume da mesma série na p. 4 do prelo), texto canônico de HOS que não está disponível no corpus deste tutorial e que, portanto, não é citado.

Sinha (2007) define operacionalmente bi- e triespectro, mas remete a Collis, White e Hammond (1998) e Fackrell et al. (1995a, 1995b) para a teoria estatística e a Hinich (1990) para a fundamentação da detecção. Esses textos não foram diretamente consultados aqui e, em conformidade com o protocolo de pesquisa acadêmica vigente, não são citados sem mediação por Sinha.

A ponte construída neste tutorial é, portanto, firme nos seus dois apoios — a representação espectral determinística de Oppenheim et al. (1997) e as definições operacionais de HOS em Sinha (2007) — mas reconhece explicitamente o vão estatístico entre eles como território a ser percorrido com literatura adicional (Nikias & Petropulu; teoria de processos estocásticos) para uma fundamentação completa. A demonstração computacional contida no caderno-companheiro [`HOS_math_tutorial.ipynb`](HOS_math_tutorial.ipynb) realiza, em sinais sintéticos, o que esta ponte argumenta em prosa: que PSDs idênticas podem conviver com biespectros radicalmente distintos quando a estrutura de fase entre componentes varia.

---

## Referências

Collis, W. B., White, P. R., & Hammond, J. K. (1998). Higher-order spectra: The bispectrum and trispectrum. *Mechanical Systems and Signal Processing*, *12*(3), 375–394. [As cited in Sinha (2007).]

Fackrell, J. W. A., White, P. R., Hammond, J. K., Pinnington, R. J., & Parsons, T. A. (1995a). The interpretation of the bispectra of vibration signals — I. Theory. *Mechanical Systems and Signal Processing*, *9*(3), 257–266. [As cited in Sinha (2007).]

Fackrell, J. W. A., White, P. R., Hammond, J. K., Pinnington, R. J., & Parsons, T. A. (1995b). The interpretation of the bispectra of vibration signals — II. Experimental results and applications. *Mechanical Systems and Signal Processing*, *9*(3), 267–274. [As cited in Sinha (2007).]

Hinich, M. J. (1990). Detecting a transient signal by bispectral analysis. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, *38*(7), 1277–1283. [As cited in Sinha (2007).]

Oppenheim, A. V., Willsky, A. S., & Nawab, S. H. (1997). *Signals and systems* (2nd ed.). Prentice Hall.

Sinha, J. K. (2007). Higher order spectra for crack and misalignment identification in the shaft of a rotating machine. *Structural Health Monitoring*, *6*(4), 325–334. https://doi.org/10.1177/1475921707082309
