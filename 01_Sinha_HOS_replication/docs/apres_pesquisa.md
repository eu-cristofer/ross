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

# Apresentação da Pesquisa

## Diagnóstico de Trinca e Desalinhamento em Sistemas Rotativos Utilizando Indicadores Bispectrais: Uma Investigação Numérica

## Rotor System Crack and Misalignment Diagnosis Using Bispectral Indicators: A Numerical Investigation


**Replicação computacional de Sinha (2007) e extensão ao desalinhamento de acoplamento**

Cristofer Antoni Souza Costa
*Mestrado em Engenharia Mecânica — POSMEC / UFU*
Orientador: Prof. Dr. Aldemir Aparecido Cavallini Junior

---

# Sumário

**Introdução: [Hipótese](#hipótese) e [Objetivo Geral](#objetivo-geral)**
**[Objetivos Específicos](#objetivos-específicos)**
  - [1. Revisão da Literatura](#1-revisão-da-literatura)
  - [2. Modelagem Numérica e Validação](#2-modelagem-numérica-e-validação)
  - [3. Campanha de Simulação Paramétrica (Phase 2)](#3-campanha-de-simulação-paramétrica-phase-2)
  - [4. Análise de Espectros de Ordem Superior](#4-análise-de-espectros-de-ordem-superior)
  - [5. Diagnóstico de Falhas e Análise de Sensibilidade](#5-diagnóstico-de-falhas-e-análise-de-sensibilidade)
  - [6. Validação Contra Literatura e Reprodutibilidade](#6-validação-contra-literatura-e-reprodutibilidade)

**[Questões Norteadoras](#questões-norteadoras)**
**[Contribuições Esperadas](#contribuições-esperadas)**
**[Delimitação do Estudo](#delimitação-do-estudo)**
**[Contato](#contato)**

---

# Hipótese

Os espectros de ordem superior aplicados a sinais de vibração obtidos por simulação numérica são capazes de revelar acoplamentos não lineares e assinaturas de fase que permitem diferenciar, de forma quantitativa, condições saudáveis, trincas em eixo e desalinhamento em máquinas rotativas, superando as limitações da análise espectral tradicional baseada apenas na PSD.

---

# Objetivo Geral

Desenvolver e avaliar uma metodologia computacional, baseada em simulações numéricas de elementos finitos (biblioteca ROSS) e análise de Espectros de Ordem Superior (bi-espectro e bicoerência), capaz de discriminar quantitativamente falhas de trinca respirante e desalinhamento em eixos rotativos, fornecendo um pipeline reprodutível e de código aberto que complemente ou reduza a dependência de bancadas experimentais.

---

# Objetivos Específicos

1. Revisão da Literatura
2. Modelagem Numérica e Validação
3. Campanha de Simulação Paramétrica (Phase 2)
4. Análise de Espectros de Ordem Superior
5. Diagnóstico de Falhas e Análise de Sensibilidade
6. Validação Contra Literatura e Reprodutibilidade

--- 

# Objetivos Específicos

## 1. Revisão da Literatura

   - Realizar uma revisão bibliográfica aprofundada sobre:
      - dinâmica de rotores;
      - modelagem de trincas e desalinhamento;
      - espectros de ordem superior;
      - técnicas de diagnóstico de falhas em máquinas rotativas.

---

# Objetivos Específicos

## 2. Modelagem Numérica e Validação

- Construir modelos de elementos finitos de um sistema rotor-mancal utilizando a biblioteca ROSS, incluindo efeitos giroscópicos, rigidez e amortecimento dos mancais.
- Implementar o modelo de trinca respirante com rigidez variável no tempo (modelo Mayes-Davies e Gash).
- Implementar o modelo de forçamento por desalinhamento com excitação harmônica em 1X, 2X e 3X.
- Validar os modelos desenvolvidos comparando frequências naturais e resposta ao desbalanceamento com dados publicados na literatura.


---

# Objetivos Específicos

## 3. Campanha de Simulação Paramétrica

- **Fase 1 (Validação):** Validar a baseline do pipeline numérico contra resultados experimentais da literatura (e.g., Sinha, 2007) avaliando a topologia dos espectros e a reprodução de características chave.
- **Fase 2 (DoE):** Somente após a validação bem-sucedida (Fase 1), projetar um estudo paramétrico sistemático (Planejamento de Experimentos) cobrindo:
  - Razão de profundidade da trinca (a/D = 0,0 a 0,5)
  - Ângulo de desalinhamento (0,0° a 2,0°)
  - Velocidade de rotação (0,5× a 1,5× velocidade crítica)
  - Razão de amortecimento (0,01 a 0,05)
- Gerar e armazenar sinais de vibração simulados em formato estruturado para as condições saudável, trinca e desalinhamento.

---

# Objetivos Específicos


## 4 Análise de Espectros de Ordem Superior

- Implementar algoritmos computacionais para estimação do bi-espectro (método direto com média por segmentos) e da bicoerência.
- Definir indicadores quantitativos de falha extraídos dos HOS:
  - Razão de Picos Bispectrais (BPR)
  - Soma da Bicoerência (BCS)
  - Entropia Bispectral (BE)
  - Bifase em frequências-chave
- Aplicar o pipeline HOS ao conjunto completo de simulações e construir a matriz de características para classificação.

---

# Objetivos Específicos

## 5 Diagnóstico de Falhas e Análise de Sensibilidade

- Avaliar a capacidade dos indicadores HOS de discriminar entre condições saudável, trinca e desalinhamento por meio de métricas de separabilidade (matriz de confusão, curvas ROC ou acurácia de classificação).
- Realizar análise de sensibilidade dos indicadores em relação à severidade da falha, velocidade de rotação e amortecimento.
- Comparar o desempenho dos indicadores HOS com indicadores tradicionais baseados em PSD.

---

# Objetivos Específicos


### 6 Validação Contra Literatura e Reprodutibilidade

- Comparar padrões de bi-espectro e bicoerência obtidos numericamente com resultados experimentais publicados, em particular Sinha (2007).
- Documentar e disponibilizar publicamente todo o código e dados (GitHub + Zenodo), garantindo reprodutibilidade completa do estudo.

---

## Questões Norteadoras

### Questão central

Os espectros de ordem superior aplicados a sinais obtidos por simulações numéricas de rotores são capazes de distinguir, de forma confiável e quantitativa, as assinaturas não lineares associadas a trinca em eixo e desalinhamento?

---

## Questões Norteadoras

### Desmembramento das questões

1. O modelo FEM via ROSS reproduz adequadamente o comportamento dinâmico de rotores com trinca respirante e desalinhamento?

    Os padrões HOS numéricos são consistentes com resultados experimentais publicados (Sinha, 2007)?

2. Quais características dinâmicas não lineares produzidas por trinca e desalinhamento podem ser identificadas por espectros de ordem superior?

3. Em que medida o bispectro e a bicoerência conseguem distinguir falhas com conteúdo espectral semelhante na PSD?

4. Quais indicadores escalares apresentam maior robustez para classificação entre rotor saudável, trincado e desalinhado?

---

## Questões Norteadoras

5. Como a severidade da falha e a velocidade de rotação influenciam os padrões bispectrais observados?

    Os indicadores HOS superam indicadores tradicionais (PSD) na discriminação de falhas com assinaturas frequenciais similares?



6. Até que ponto uma abordagem numérica com ferramentas open source pode fornecer resultados comparáveis aos reportados em estudos experimentais da literatura?

    A metodologia proposta é robusta o suficiente para diferentes configurações de parâmetros e níveis de ruído?

---

## Contribuições Esperadas

- Propor um fluxo metodológico integrado entre modelagem numérica em rotores e análise por espectros de ordem superior.

- Produzir uma base reprodutível de sinais simulados para estudo de falhas em máquinas rotativas.

- Estabelecer indicadores quantitativos para diferenciação entre trinca em eixo e desalinhamento.

- Fortalecer o uso de ferramentas open source no contexto de diagnóstico de falhas e monitoramento de condição.

- Gerar resultados com potencial de publicação científica em periódicos da área de dinâmica, vibrações e monitoramento estrutural.

---


## Delimitação do Estudo

Este trabalho terá foco em uma investigação numérica. A validação será conduzida prioritariamente por comparação com resultados já publicados na literatura, não incluindo, em um primeiro momento, uma campanha experimental própria. O escopo inicial concentra-se nas falhas de trinca em eixo e desalinhamento, podendo ser expandido futuramente para outras condições, como desbalanceamento, folgas ou defeitos em mancais.

---

# Contato

Cristofer Antoni Souza Costa
https://github.com/eu-cristofer
cristofer@petrobras.com.br
cristoferantoni@ufu.br