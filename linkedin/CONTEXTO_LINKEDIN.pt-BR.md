# EEG Signal Processing Lab: documento de contexto para o LinkedIn

> **Idioma:** Português (Brasil) · English version: [`LINKEDIN_CONTEXT.en.md`](LINKEDIN_CONTEXT.en.md)
> **Última atualização:** 2026-10-29
> **Versão do projeto coberta:** v1.0.0 (commit `13d2ca2`, 2026-06-08)
> **Repositório:** https://github.com/jevrton-code/eeg-signal-processing-lab

---

## 0. Para que serve este documento

Este arquivo é a **fonte única de contexto** para tudo o que for publicado sobre
este projeto no LinkedIn: posts, carrosséis (posts de documento em PDF),
comentários, atualizações de versão e a seção "Projetos" do perfil. Ele pode
ser usado por você ou entregue inteiro a um assistente de IA.

Tudo aqui foi conferido contra o repositório (código, saídas dos notebooks,
figuras, testes e histórico do git) em 2026-10-29. Onde um número foi derivado
e não aparece escrito no README, isso está indicado.

**Como usar**

- **Para escrever um post:** leia §1 (resumos prontos), §5 (o que os
  resultados significam) e §6 (o que não afirmar), e escolha um ângulo em §12.
- **Para pedir a um assistente de IA:** entregue este arquivo e diga qual
  ângulo da §12 você quer, o idioma e o tamanho. Instrua-o a usar **apenas** os
  números da §4 e a respeitar a §6.
- **Quando o projeto mudar:** atualize primeiro a §4 (ficha técnica), a §8
  (linha do tempo) e a §20 (registro de alterações).

**Regras inegociáveis para qualquer texto público**

1. Números só da ficha técnica (§4), sempre com o contexto "sujeitos 1–3,
   runs 1, 2, 4, 8 e 12".
2. Nada de interpretação clínica, diagnóstica ou cognitiva. O projeto é
   educacional e exploratório.
3. O aumento de alfa com olhos fechados é um **padrão esperado e conhecido**,
   reproduzido como teste de sanidade. Não é uma descoberta.
4. Não há classificador neste projeto. A classificação está no projeto irmão
   (BCI Motor Imagery Classifier, §17).
5. Creditar o dataset e o MNE-Python (§15).

---

## 1. Resumos prontos (do mais curto ao mais longo)

**Uma linha (bio, legenda de imagem, título de carrossel)**

> Laboratório reprodutível de processamento de sinais de EEG: carregamento,
> pré-processamento, épocas e análise espectral com MNE-Python e dados
> públicos.

**Gancho (cabe antes do "ver mais")**

> Antes de treinar qualquer modelo com EEG, construí um projeto inteiro só
> para entender o sinal. A primeira armadilha estava num rótulo: "T1" não
> significa sempre a mesma coisa.

**Gancho alternativo (resultado visual)**

> Fechar os olhos multiplicou a potência alfa occipital por cerca de 19 nos
> meus dados. É um efeito conhecido desde 1929, e foi o meu teste de sanidade.

**Resumo curto (para post rápido ou comentário)**

> Construí um laboratório reprodutível de processamento de EEG com MNE-Python,
> usando dados públicos do PhysioNet (3 sujeitos, 64 canais, 160 Hz). O fluxo
> vai do sinal bruto até a análise espectral: inspeção, pré-processamento
> conservador (1–40 Hz, referência média), mapeamento de eventos por tipo de
> run, épocas e PSD. O teste de sanidade, o aumento de alfa occipital com
> olhos fechados, apareceu nos três sujeitos. Sem classificador e sem
> promessas: primeiro entender o sinal.

**Descrição para a seção "Projetos" do perfil (cerca de 1.530 caracteres;
limite do LinkedIn: 2.000)**

```text
Laboratório reprodutível de processamento de sinais de EEG, construído como base para trabalhos em interfaces cérebro-computador (BCI) e neurotecnologia.

O que fiz
• Carreguei e inspecionei dados públicos do PhysioNet EEG Motor Movement/Imagery Dataset com MNE-Python (sujeitos 1–3; runs de linha de base e de imagética motora; 64 canais, 160 Hz), conferindo os fatos do dataset em vez de assumi-los.
• Mapeei os eventos T0/T1/T2 de acordo com o tipo de run, porque o mesmo código muda de significado entre runs; o código se recusa a adivinhar um mapeamento.
• Apliquei pré-processamento conservador e documentado: montagem 10-05, filtro passa-banda de 1–40 Hz e referência média, com evidência antes/depois. Dispensei o filtro notch com base na própria evidência e adiei o ICA, com justificativa escrita.
• Criei épocas alinhadas ao estímulo (−0,5 a +4,0 s), tabelas de contagem de eventos e análise espectral (PSD) com mapas topográficos de alfa e beta.
• Organizei a lógica num pacote Python testável (28 testes passando), com dois notebooks reprodutíveis e um relatório HTML gerado automaticamente.

Resultado de sanidade
O aumento esperado de alfa (8–13 Hz) occipital com olhos fechados apareceu nos três sujeitos: razão de potência olhos fechados/abertos de 19,46 na média geral.

Escopo honesto: é um projeto educacional e exploratório com 3 sujeitos. Não tem classificador, não faz interpretação clínica e não generaliza para o dataset completo.

Stack: Python, MNE-Python, NumPy, SciPy, pandas, Matplotlib, Jupyter, pytest.
```

**Campos sugeridos da seção "Projetos"**

| Campo | Sugestão |
| --- | --- |
| Nome do projeto | EEG Signal Processing Lab: processamento reprodutível de EEG com MNE-Python |
| Data | jun. de 2026 (v1.0 publicada em 2026-06-08) |
| Competências | Python · Processamento de sinais · Eletroencefalografia (EEG) · MNE-Python · Análise de dados |
| Mídia | Link do repositório + `figures/psd_baseline_comparison.png` (ver §10) |
| Associado a | [A PREENCHER: experiência, curso ou "projeto pessoal"] |

---

## 2. O problema e a motivação

### Em linguagem simples

O **EEG** registra a atividade elétrica do cérebro por eletrodos no couro
cabeludo. O sinal é fraco (dezenas de microvolts), ruidoso e cheio de
interferências: piscadas, movimentos, a rede elétrica. Antes de qualquer
modelo de IA, é preciso saber carregar, limpar, segmentar e analisar esse sinal
sem distorcê-lo.

### Por que começar pela base

Projetos de BCI costumam pular direto para o classificador. Este projeto faz o
contrário: mostra maturidade com dados neurais (carregamento, mapeamento de
eventos, filtragem, visualização, consciência sobre artefatos,
reprodutibilidade e interpretação honesta) antes de construir qualquer modelo.
Nas palavras do `ROADMAP.md`: "o sinal é entendido e documentado antes de
qualquer modelo ser construído em cima dele".

### Motivação pessoal do autor

[A PREENCHER: por que você quis construir isto, de onde vem seu interesse em
EEG/neurotecnologia, o que queria aprender. Ver §19.]

---

## 3. O que foi construído

### Visão geral do fluxo

```text
PhysioNet EEGMMIDB v1.0.0 (EDF+, via mne.datasets.eegbci)
  └─ Recorte da v1: sujeitos 1–3 × runs 1, 2, 4, 8, 12  (15 gravações)
      └─ Notebook 01 — carregamento e inspeção
      │    • padronização dos nomes dos canais ("Fcz." → "FCz")
      │    • confirmação de 64 canais @ 160 Hz e das durações
      │    • mapeamento de T0/T1/T2 POR TIPO DE RUN
      │    • figuras: sinal bruto, montagem, distribuição e linha do tempo de eventos
      └─ Notebook 02 — pré-processamento, épocas e PSD
           • montagem standard_1005 → passa-banda 1–40 Hz (FIR) → referência média
           • sem notch (60 Hz removido pelo passa-baixa de 40 Hz) · ICA adiado
           • épocas de −0,5 a +4,0 s com linha de base (None, 0)
           • PSD de Welch: olhos abertos × fechados nos canais O1/Oz/O2
           • mapas topográficos de alfa e beta
  └─ eeg_lab.report → relatório HTML autocontido (gerado localmente)
```

### O mapeamento de eventos por tipo de run (o detalhe crítico)

Os arquivos usam os códigos T0, T1 e T2, mas o significado de T1/T2 **muda de
acordo com o run**:

| Código | Run 1 (olhos abertos) | Run 2 (olhos fechados) | Runs 4, 8, 12 (imagética esq./dir.) |
| --- | --- | --- | --- |
| T0 | repouso (olhos abertos) | repouso (olhos fechados) | repouso |
| T1 | — | — | punho esquerdo (imaginado) |
| T2 | — | — | punho direito (imaginado) |

Nos runs de punhos/pés do dataset (como 6, 10 e 14), T1/T2 significam "ambos
os punhos" e "ambos os pés". Por isso a função `map_events_by_run` recebe o **número do
run** e lança um erro para qualquer run fora do recorte, em vez de adivinhar
um rótulo.

### Organização do código

- `src/eeg_lab/`: pacote com lógica pura e testável: `config` (recorte,
  constantes de filtro, épocas e bandas), `data` (carregamento via MNE),
  `preprocessing`, `spectral` (PSD e potência de banda), `visualization` e
  `report` (montagem do relatório HTML).
- `notebooks/01_eeg_signal_processing_lab.ipynb`: carregamento e inspeção.
- `notebooks/02_preprocessing_epochs_psd.ipynb`: pré-processamento, épocas e
  PSD.
- `tests/`: testes de configuração, mapeamento de eventos, épocas e funções
  espectrais (não precisam de rede nem de dados).
- `figures/`: 8 figuras versionadas.

### Como rodar

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_eeg_signal_processing_lab.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_preprocessing_epochs_psd.ipynb
python -m eeg_lab.report   # -> reports/eeg_signal_processing_report.html
pytest -q
```

---

## 4. Ficha técnica (números verificados)

### Dataset e recorte

| Item | Valor | Fonte |
| --- | --- | --- |
| Dataset | PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0 | `README.md` |
| DOI | 10.13026/C28G6P | `README.md` |
| Formato | EDF+ com canal de anotações; adquirido com BCI2000 | `README.md` |
| Canais / amostragem | 64 EEG @ 160 Hz (confirmado nos 15 arquivos) | saída do notebook 01 |
| Runs por sujeito no dataset | 14 | `README.md` |
| Sujeitos da v1 | 1, 2, 3 | `config.SUBJECTS` |
| Runs da v1 | 1 (olhos abertos), 2 (olhos fechados), 4, 8, 12 (imagética esq./dir.) | `config.RUNS` |
| Gravações analisadas | 15 (3 sujeitos × 5 runs) | notebook 01 |
| Duração dos runs de linha de base | 60,99 s | notebook 01 |
| Duração dos runs de imagética | 122,99 a 124,99 s (média 124,32 s) | notebook 01 |
| Anotações por run de imagética | 30 | notebook 01 |
| Licença do código | MIT | `LICENSE` |
| Licença do dataset | ODC-By 1.0 (dados não redistribuídos) | `CITATION.md` |

### Contagem de eventos (sujeitos 1–3, runs 1, 2, 4, 8, 12)

| Condição | Total | Por run de imagética (somando os 3 sujeitos) |
| --- | ---: | ---: |
| Repouso (nos runs de imagética) | 135 | 45 |
| Punho esquerdo (imaginado) | 69 | 23 |
| Punho direito (imaginado) | 66 | 22 |
| Repouso, olhos abertos (run 1) | 3 | — |
| Repouso, olhos fechados (run 2) | 3 | — |

### Pré-processamento e épocas

| Parâmetro | Valor | Justificativa resumida |
| --- | --- | --- |
| Montagem | `standard_1005` (10-05) | Posições conhecidas para mapas topográficos |
| Passa-banda | 1–40 Hz (FIR) | 1 Hz remove deriva lenta; 40 Hz mantém alfa e beta e fica abaixo do Nyquist (80 Hz) |
| Referência | Média | Convenção documentada, não "verdade" |
| Notch | Não aplicado | O passa-baixa de 40 Hz já atenua os 60 Hz da rede elétrica (EUA); evidência na figura antes/depois |
| ICA | Adiado | Justificativa escrita; fora do escopo da v1 |
| Canais ruins | Tratamento manual/sinalizado, não automatizado | Decisão de projeto |
| Janela das épocas | −0,5 a +4,0 s, linha de base (None, 0) | Cobre o período de tarefa de cerca de 4,1 s |
| Exemplo de épocas (sujeito 1, run 4) | 29 épocas: 14 repouso, 8 esquerdo, 7 direito | notebook 02 |
| Bandas | delta 1–4, teta 4–8, alfa 8–13, beta 13–30, gama 30–40 Hz | `config.FREQ_BANDS` |
| PSD | Welch, 1–40 Hz | notebook 02 |

### Resultado do teste de sanidade: alfa occipital (O1/Oz/O2), olhos fechados ÷ olhos abertos

| Sujeito | Razão de potência alfa (8–13 Hz) |
| --- | ---: |
| 1 | 22,84 |
| 2 | 9,17 |
| 3 | 26,49 |
| **Média geral (PSD média dos 3 sujeitos)** | **19,46** |

- A razão da média geral é calculada sobre as curvas de PSD médias dos três
  sujeitos, não pela média das três razões.
- *Derivado:* é uma razão de **potência**. Em amplitude, equivale a cerca de
  4,4 vezes (raiz quadrada de 19,46). Use "potência" sempre que citar o 19.
- O mapa topográfico (sujeito 1, run 2) mostra alfa concentrado na região
  posterior, como esperado.

### Tamanho e qualidade

- Cerca de 1.690 linhas de Python (pacote e testes).
- 6 módulos, 2 notebooks, 8 figuras versionadas.
- **Testes: 28 passando, 1 pulado** (teste de integração que exige os dados
  baixados localmente). Verificado em 2026-10-29.
- Relatório HTML de cerca de 2,2 MB, **não versionado** (fica acima do limite
  de cerca de 2 MB que o projeto adota para binários); é regenerado com
  `python -m eeg_lab.report`.
- Versão do MNE-Python registrada nas saídas dos notebooks: 1.12.1.

---

## 5. Resultados e interpretação (as histórias que os números contam)

### 5.1 O teste de sanidade funcionou nos três sujeitos

Ao fechar os olhos, a potência alfa occipital normalmente aumenta. É um dos
efeitos mais antigos e robustos do EEG, descrito por Hans Berger em 1929.
Aqui ele apareceu nos três sujeitos (razões de 9,17 a 26,49). **Isso não é uma
descoberta:** é a prova de que o pipeline de carregamento, filtragem e PSD está
correto. Essa é a forma certa de apresentar o resultado.

### 5.2 A variação entre pessoas aparece até num efeito "garantido"

O sujeito 2 teve razão de 9,17; o sujeito 3, de 26,49. Mesmo um efeito clássico
varia quase três vezes entre pessoas. É a mesma mensagem do projeto irmão de
BCI: médias escondem indivíduos.

### 5.3 Uma decisão baseada em evidência: o filtro que não entrou

O plano previa avaliar um filtro notch para os 60 Hz da rede elétrica. A
figura antes/depois mostra o pico de 60 Hz no sinal bruto e mostra que o
passa-baixa de 40 Hz já o elimina. Resultado: nenhum filtro desnecessário
entrou no pipeline. É um exemplo concreto de "inspecionar antes de decidir".

### 5.4 O sinal é ruidoso, e o projeto diz isso

As épocas médias (C3/Cz/C4, cerca de 7–8 tentativas por condição num run) são
ruidosas. O notebook afirma explicitamente que **não** se trata de um efeito
evocado estabelecido, e sim da prova de que épocas e rótulos funcionam de ponta
a ponta.

---

## 6. O que pode e o que não pode ser dito

| ✅ Pode dizer | ❌ Não diga | Por quê |
| --- | --- | --- |
| "Reproduzi o aumento esperado de alfa com olhos fechados como teste de sanidade" | "Descobri que..." / "Meu projeto mostra que o cérebro..." | É um efeito conhecido desde 1929. |
| "Razão de potência alfa de 19,46 na média geral de 3 sujeitos" | "Alfa 19 vezes maior" sem dizer "potência" | Em amplitude, a razão é cerca de 4,4. |
| "Projeto educacional e exploratório" | Qualquer interpretação clínica, diagnóstica ou cognitiva | O README exclui isso explicitamente. |
| "Base para trabalhos de BCI" | "Construí um BCI" / "classificador de EEG" | Não há classificador neste projeto. |
| "Pipeline reprodutível e testado (28 testes)" | "100% testado" | Os testes cobrem a lógica pura; notebooks e figuras não têm testes automatizados. |
| "Dados públicos do PhysioNet, 3 sujeitos" | "Dataset de 109 sujeitos analisado" | Só o recorte da v1 foi analisado. |
| "Pré-processamento conservador e documentado" | "Pré-processamento otimizado" / "removi todos os artefatos" | Não há ICA nem remoção de artefatos na v1. |

---

## 7. Decisões de engenharia (bastidores que viram conteúdo)

1. **Mapeamento de eventos pelo número do run, nunca só pelo código.** É a
   falha mais comum com este dataset. A função lança erro para runs fora do
   recorte em vez de adivinhar.
2. **Confirmar em vez de assumir.** O notebook 01 verifica 64 canais, 160 Hz e
   as durações de cada arquivo, em vez de confiar na documentação.
3. **Padronizar os nomes dos canais** (`mne.datasets.eegbci.standardize`, que
   corrige coisas como "Fcz." → "FCz") para que a montagem 10-05 se encaixe.
4. **Pré-processamento conservador.** 1–40 Hz e referência média, cada
   parâmetro com justificativa; nada de "otimizar" filtros sem critério.
5. **Notch inspecionado e dispensado com evidência** (figura antes/depois).
6. **ICA adiado de propósito**, com justificativa escrita. Saber o que não
   fazer ainda também é uma decisão.
7. **Notebooks orquestram; o pacote contém a lógica.** Funções puras em
   `eeg_lab` são testáveis sem rede e sem dados.
8. **Higiene de repositório.** Dados brutos nunca entram no git (`data/raw/` e
   extensões de EEG no `.gitignore`); o relatório HTML de 2,2 MB é regenerado
   em vez de versionado; só as figuras-fonte são versionadas.
9. **Licenças separadas.** Código MIT; dados ODC-By 1.0, com atribuição
   completa no `CITATION.md`.
10. **Entregas em versões.** v0.1 (estrutura e documentação) → v0.2 (primeiro
    notebook) → v0.3 (pré-processamento, épocas, PSD) → v1.0 (relatório e
    polimento).
11. **Documentação pública enxuta.** A pasta `docs/` foi removida e a
    informação essencial ficou no README, no ROADMAP e no relatório gerado.

---

## 8. Linha do tempo

| Data | Versão | Commit | O que entrou |
| --- | --- | --- | --- |
| 2026-06-08 | v0.1 | `4c3c19a` | Estrutura, documentação, citação, roadmap |
| 2026-06-08 | v0.2 | `0333f29` | Primeiro notebook reprodutível (sujeitos 1–3, runs 1, 2, 4, 8, 12) |
| 2026-06-08 | v0.3 | `ff241e9` | Pré-processamento conservador, eventos e épocas |
| 2026-06-08 | v0.3 | `5760388` | PSD olhos abertos × fechados e análise de bandas |
| 2026-06-08 | v1.0 | `2848f46` | Relatório reprodutível e polimento final |
| 2026-06-08 | — | `1e8cc17` | URL do GitHub atualizada no README |
| 2026-06-08 | — | `13d2ca2` | Pasta `docs/` removida; documentação pública enxuta |

Não há tag nem *release* criada no GitHub (ver §18).

---

## 9. Stack e competências

**Tecnologias:** Python 3.11+, MNE-Python (≥ 1.6; notebooks executados com
1.12.1), NumPy, SciPy, pandas, Matplotlib, Jupyter, pytest, ruff.

**Competências para marcar no LinkedIn**

- Python
- Processamento de sinais (Signal Processing)
- Eletroencefalografia (EEG)
- MNE-Python
- Análise espectral / Análise de séries temporais
- Jupyter
- Análise de dados
- Pesquisa reprodutível
- Neurociência
- Neurotecnologia

**Competências demonstradas, em linguagem de recrutador**

- Trabalhar com dados científicos reais, ruidosos e com armadilhas de
  documentação.
- Tomar decisões técnicas com base em evidência e registrá-las.
- Transformar análise exploratória em código testável e reprodutível.
- Comunicar limites com clareza.

---

## 10. Ativos visuais disponíveis

| Arquivo | O que mostra | Melhor uso | Cuidados |
| --- | --- | --- | --- |
| `figures/psd_baseline_comparison.png` (1088×591) | PSD occipital olhos abertos × fechados, com a faixa alfa destacada | **Imagem principal.** O pico de alfa em vermelho é imediato. | Explicar que é o padrão esperado. |
| `figures/preprocessing_before_after.png` (1088×536) | PSD antes e depois do pré-processamento, com o pico de 60 Hz no bruto | Post sobre o notch dispensado | Linguagem técnica; precisa de legenda explicativa. |
| `figures/raw_signal_preview.png` (1197×646) | 10 s de EEG bruto em 10 canais | Capa ou abertura ("é assim que o EEG chega") | Sem filtro: mostra deriva e artefatos, de propósito. |
| `figures/events_timeline_subject1_run4.png` (1198×448) | Linha do tempo de repouso e punho esquerdo/direito num run | Post sobre o mapeamento T0/T1/T2 | A legenda cobre parte de duas barras verdes. |
| `figures/band_topomap_eyes_closed.png` (531×177) | Mapas topográficos de alfa e beta | Complemento visual | **Resolução muito baixa** para o LinkedIn; regere com DPI maior antes de usar. |
| `figures/channel_layout.png` (884×892) | Montagem de 64 canais | Explicar o que é EEG | Quase quadrada; boa para carrossel. |
| `figures/epochs_example.png` (1374×457) | Épocas médias em C3/Cz/C4 | Post sobre "ruído é honesto" | Ruidosa; nunca apresentar como efeito. |
| `figures/event_distribution.png` (978×536) | Contagem de eventos por condição | Post sobre o recorte de dados | Pouco impacto visual sozinha. |

**Roteiro sugerido de carrossel (8 slides, 1080×1350)**

1. Capa: "Antes do modelo, o sinal" + nome do projeto.
2. O que é EEG, com `raw_signal_preview.png`.
3. A armadilha do T1/T2 (tabela da §3).
4. Pré-processamento em 3 passos (montagem → 1–40 Hz → referência média).
5. O filtro que não entrou (`preprocessing_before_after.png`).
6. O teste de sanidade (`psd_baseline_comparison.png` + razões por sujeito).
7. O que este projeto NÃO faz (§6).
8. Próximo passo: o benchmark de BCI + link do GitHub + créditos.

**Ativos que faltam:** imagem de *social preview* do GitHub (1280×640);
topomapa em alta resolução; versão do relatório HTML acessível on-line (por
exemplo via GitHub Pages) ou exportada em PDF para um post de documento.

---

## 11. Público, posicionamento e tom

### Para quem os posts falam

| Público | O que procura | O que destacar |
| --- | --- | --- |
| Recrutadores e gestores técnicos | Rigor e capacidade de lidar com dados reais | Decisões documentadas, testes, reprodutibilidade |
| Pessoas de dados e engenharia | Boas práticas | Lógica pura testável, notebooks como orquestração, higiene de repositório |
| Comunidade de neurotecnologia e EEG | Domínio técnico | Mapeamento por run, montagem 10-05, referência média, notch e ICA |
| Estudantes | Aprender EEG na prática | Passo a passo do pipeline, glossário |
| Público geral curioso | Entender o que é EEG | Efeito alfa de olhos fechados (experimento que qualquer um entende) |

### Posicionamento sugerido

> Engenharia de software aplicada à neurotecnologia: entender o sinal antes de
> construir o modelo, com dados públicos, decisões documentadas e limites
> claros.

### Tom de voz

- Primeira pessoa, curioso e didático.
- O "fracasso" honesto (sinal ruidoso, efeito que varia) é conteúdo.
- Evitar "decodificar o cérebro", "ler pensamentos" e similares.
- Parágrafos curtos; poucos emojis, se algum.

### Notas de formato do LinkedIn (confira, os limites mudam)

- Post: até 3.000 caracteres; o gancho precisa caber nas primeiras linhas
  (cerca de 200 caracteres) antes do "ver mais".
- Descrição na seção "Projetos": até 2.000 caracteres.
- Carrossel: post de documento em PDF com slides verticais (1080×1350) ou
  quadrados.
- Hashtags: 3 a 5 relevantes.

---

## 12. Banco de ângulos para posts

### A. Lançamento: antes do modelo, o sinal
- **Gancho:** "Antes de treinar qualquer modelo com EEG, construí um projeto
  inteiro só para entender o sinal."
- **Pontos:** o fluxo do bruto à PSD; decisões documentadas; teste de
  sanidade; sem classificador de propósito.
- **Visual:** carrossel da §10 ou `psd_baseline_comparison.png`.
- **CTA:** link do GitHub.

### B. T1 nem sempre é T1
- **Gancho:** "O mesmo código de evento significa coisas diferentes no mesmo
  dataset. Meu código se recusa a adivinhar."
- **Pontos:** tabela T0/T1/T2; runs 4/8/12 × 6/10/14; `ValueError` para runs
  fora do recorte; lição geral sobre metadados.
- **Visual:** `events_timeline_subject1_run4.png`.
- **Público:** dados e engenharia.

### C. Feche os olhos (o efeito de Berger)
- **Gancho:** "Fechar os olhos multiplicou a potência alfa por cerca de 19 nos
  meus dados. E isso não é uma descoberta."
- **Pontos:** efeito descrito desde 1929; razões por sujeito; potência ×
  amplitude; por que um teste de sanidade vale mais que um resultado novo.
- **Visual:** `psd_baseline_comparison.png`.
- **Público:** geral e neurotecnologia.

### D. O filtro que eu não usei
- **Gancho:** "Eu ia adicionar um filtro. A evidência disse que não
  precisava."
- **Pontos:** pico de 60 Hz no sinal bruto; o passa-baixa de 40 Hz já o
  elimina; inspecionar antes de decidir.
- **Visual:** `preprocessing_before_after.png`.

### E. Saber o que adiar
- **Gancho:** "Deixei o ICA de fora. De propósito."
- **Pontos:** escopo da v1; justificativa escrita; diferença entre "não fiz" e
  "decidi não fazer agora".

### F. Confie, mas confirme
- **Gancho:** "A documentação dizia 64 canais e 160 Hz. Conferi mesmo assim."
- **Pontos:** verificação dos 15 arquivos; nomes de canais corrigidos
  ("Fcz." → "FCz"); durações registradas.

### G. Notebooks não são o produto
- **Gancho:** "Meus notebooks não têm lógica. Ela vive num pacote com 28
  testes."
- **Pontos:** separação entre orquestração e lógica; testes sem rede e sem
  dados; teste de integração que roda só quando os dados existem.
- **Público:** engenharia e dados.

### H. Ruído é honesto
- **Gancho:** "Este gráfico é feio. E está certo."
- **Pontos:** épocas médias com 7–8 tentativas; por que não chamar isso de
  efeito; maturidade na interpretação.
- **Visual:** `epochs_example.png`.

### I. O que não entra no git
- **Gancho:** "Meu relatório tem 2,2 MB e não está no repositório."
- **Pontos:** dados brutos nunca versionados; relatório regenerável; só
  figuras-fonte no git; licenças separadas.

### J. Série: do sinal ao classificador
- **Gancho:** "Primeiro entendi o sinal. Depois tentei classificá-lo."
- **Pontos:** ligação com o BCI Motor Imagery Classifier, mesmo dataset (§17).

---

## 13. Glossário para linguagem acessível

| Termo | Explicação simples |
| --- | --- |
| **EEG** | Registro da atividade elétrica do cérebro por eletrodos no couro cabeludo. |
| **Canal / eletrodo** | Cada ponto de medição no couro cabeludo. Aqui são 64. |
| **Montagem 10-05** | Mapa padronizado das posições dos eletrodos na cabeça. |
| **Filtro passa-banda** | Mantém só as frequências de interesse (aqui, 1 a 40 Hz). |
| **Filtro notch** | Remove uma frequência específica, como os 60 Hz da rede elétrica. |
| **Referência média** | Mede cada eletrodo em relação à média de todos. |
| **ICA** | Técnica que separa o sinal em componentes, usada para remover piscadas e outros artefatos. |
| **Artefato** | Sinal que não vem do cérebro: piscadas, músculos, rede elétrica. |
| **Época** | Recorte do sinal alinhado a um evento (aqui, de −0,5 a +4 s em torno de cada estímulo). |
| **PSD (densidade espectral de potência)** | Quanto de "energia" o sinal tem em cada frequência. |
| **Banda alfa (8–13 Hz)** | Ritmo que aumenta na região occipital quando fechamos os olhos e relaxamos. |
| **Banda beta (13–30 Hz)** | Ritmo associado, entre outras coisas, a atividade motora. |
| **Mapa topográfico** | Mapa da cabeça vista de cima, colorido pela potência em cada região. |
| **Imagética motora** | Imaginar um movimento sem executá-lo. |
| **T0 / T1 / T2** | Códigos de evento do dataset; o significado de T1/T2 depende do run. |

---

## 14. Hashtags e palavras-chave

**Hashtags (escolha de 3 a 5 por post)**

- Núcleo: `#EEG` `#ProcessamentoDeSinais` `#Neurotecnologia` `#Python`
  `#MNEPython`
- Alcance em português: `#Neurociência` `#CiênciaDeDados`
  `#InterfaceCérebroComputador`
- Alcance em inglês: `#SignalProcessing` `#Neurotechnology` `#Neuroscience`
  `#OpenScience` `#BCI`

**Palavras-chave para busca e SEO do perfil:** EEG, processamento de sinais,
MNE-Python, PSD, análise espectral, banda alfa, pré-processamento de EEG,
épocas, PhysioNet, neurotecnologia, interface cérebro-computador.

---

## 15. Créditos e citações

**Linha curta para colocar no fim de um post**

> Dados: PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004;
> doi:10.13026/C28G6P), licença ODC-By 1.0. Análise com MNE-Python (Gramfort
> et al., 2013).

**Referências completas** (detalhes e BibTeX em `CITATION.md`)

- Schalk, G. et al. (2004). BCI2000: A General-Purpose Brain-Computer
  Interface (BCI) System. *IEEE Trans. Biomed. Eng.*, 51(6), 1034–1043.
- Goldberger, A. L. et al. (2000). PhysioBank, PhysioToolkit, and PhysioNet.
  *Circulation*, 101(23), e215–e220.
- EEG Motor Movement/Imagery Dataset (v1.0.0). PhysioNet (2009).
  https://doi.org/10.13026/C28G6P
- Gramfort, A. et al. (2013). MEG and EEG Data Analysis with MNE-Python.
  *Front. Neurosci.*, 7, 267.

**Links úteis**

- Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MNE-Python: https://mne.tools/

---

## 16. Roadmap e gatilhos de atualização

Itens adiados de propósito (`ROADMAP.md`) e o post que cada um permitiria:

| Entrega futura | Post que ela permite |
| --- | --- |
| Classificador de imagética motora | Já existe como projeto separado (BCI Motor Imagery Classifier). Post de ligação entre os dois. |
| Benchmark cross-subject com os 109 sujeitos | "O efeito alfa se mantém em 109 pessoas?" |
| Deep learning (Braindecode, EEGNet) | "Depois da base, os modelos" |
| Dashboard de biossinais em tempo real / controle BCI | Mudança de escopo: offline → online |
| Integração com BrainFlow e hardware | "Do dataset público ao meu próprio EEG" |
| Explorador visual (Streamlit / Next.js) | Demo interativa: ótimo material visual |
| ICA e tratamento de artefatos | "Removendo piscadas: antes e depois" |

**Regra:** toda atualização deve citar o recorte usado e comparar com os
números da v1 (§4) quando fizer sentido.

---

## 17. Conexão com o portfólio

Este é um de três projetos públicos que formam uma narrativa coerente:

| Projeto | Pergunta que responde | Data |
| --- | --- | --- |
| **EEG Signal Processing Lab** (este) | Como carregar, inspecionar, pré-processar e analisar EEG de forma responsável? | jun. 2026 |
| [BCI Motor Imagery Classifier](https://github.com/jevrton-code/bci-motor-imagery-classifier) | Dá para classificar imagética motora, e como avaliar isso com honestidade? | jun. 2026 |
| [FlyWire Propagation Sim](https://github.com/jevrton-code/flywire-propagation-sim) | Como a atividade se espalha por um circuito neural real, mapeado sinapse a sinapse? | ago. 2026 |

**O fio condutor:** dados públicos reais, reprodutibilidade, engenharia de
software disciplinada e honestidade sobre os limites. Este projeto e o de BCI
usam o **mesmo dataset**: aqui se entende o sinal, lá se constroem e avaliam
classificadores. O FlyWire sai do sinal medido no couro cabeludo e vai para o
diagrama de fiação do cérebro, com uma aplicação full-stack.

**Post de portfólio possível:** "Três projetos, uma regra: escrever o que o
modelo não faz antes de mostrar o que ele faz."

---

## 18. Pendências encontradas antes de divulgar

1. **Topomapa em baixa resolução** (531×177): regerar com DPI maior
   (`save_figure` usa 110 por padrão).
2. **Relatório HTML não acessível on-line.** Quem vem do LinkedIn não consegue
   vê-lo sem rodar o projeto. Opções: GitHub Pages, um PDF do relatório ou um
   link para os notebooks renderizados no GitHub.
3. **Sem tag nem release no GitHub.** Criar a release `v1.0.0` dá um link
   estável para anunciar.
4. **Autor genérico no `pyproject.toml`** ("eeg-signal-processing-lab
   contributors"). Opcional: colocar seu nome.
5. **Sem imagem de *social preview*** configurada no GitHub.
6. **Legenda sobreposta** em `events_timeline_subject1_run4.png` (cobre parte
   de duas barras).
7. O `ROADMAP.md` menciona uma "página de limitações finalizada"; depois da
   remoção de `docs/`, as limitações vivem no README e no relatório. Vale
   ajustar o texto.

---

## 19. Contexto pessoal a preencher (o que o repositório não sabe)

- **Por que este projeto:** [A PREENCHER]
- **Sua formação e trajetória até aqui:** [A PREENCHER]
- **Tempo dedicado e contexto** (projeto pessoal, curso, transição de
  carreira): [A PREENCHER]
- **O que foi mais difícil ou mais surpreendente:** [A PREENCHER]
- **Ferramentas usadas no processo**, incluindo assistentes de IA, se quiser
  mencionar: [A PREENCHER]
- **Objetivo profissional** (tipo de vaga, área, empresas de interesse):
  [A PREENCHER]
- **Pessoas ou comunidades para agradecer ou marcar:** [A PREENCHER]
- **URL do seu perfil no LinkedIn:** [A PREENCHER]

---

## 20. Registro de alterações deste documento

| Data | Alteração |
| --- | --- |
| 2026-10-29 | Versão inicial, cobrindo o projeto na v1.0.0 (`13d2ca2`). Números conferidos contra as saídas dos notebooks; testes executados localmente (28 passando, 1 pulado). |
