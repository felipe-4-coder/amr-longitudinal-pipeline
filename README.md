# AMR Longitudinal Pipeline

Pipeline de vigilância genômica para monitoramento longitudinal de genes de 
resistência antimicrobiana (AMR) em bactérias ao longo do tempo.

## Visão do Projeto

Este projeto nasce como evolução natural do [NCBI Downloader](https://github.com/felipe-4-coder/ncbi-downloader), 
com o objetivo de responder uma pergunta biológica específica:

> **Como a prevalência de genes de resistência antimicrobiana em 
> *Klebsiella pneumoniae* evoluiu entre 2000 e 2026?**

## Arquitetura do Pipeline

1. Download      → genomas de K. pneumoniae por ano via datasets.exe (NCBI)
2. QC            → controle de qualidade dos assemblies via CheckM
3. AMR Detection → identificação de genes de resistência via BLAST + CARD
4. Consolidação  → agrega prevalência de genes AMR por ano
5. Visualização  → dashboard interativo com evolução temporal

## O que esse projeto faz

### `download_genomes.py`
Realiza o download automatizado de genomas de um organismo específico diretamente 
do NCBI, filtrando por ano (2000-2026) e priorizando assemblies RefSeq de nível 
Complete Genome. Para cada ano, gera um arquivo `.zip` separado na pasta de saída.

### `qc_filter.py`
Realiza controle de qualidade sobre os genomas baixados, filtrando por nível de 
montagem, N50 e tamanho total do genoma. Genomas aprovados são organizados por ano 
em `data/approved/`. Arquivos corrompidos são ignorados automaticamente.

### `run_amr_pipeline.py`
Automatiza a execução do BLAST em todos os genomas aprovados, comparando cada um 
contra o banco de dados CARD. Gera um arquivo de resultado por genoma organizado 
por ano em `data/results/`.

### `consolidate.py`
Percorre todos os resultados do BLAST e consolida a contagem de genes de resistência 
por ano em uma tabela CSV (`amr_longitudinal.csv`), pronta para visualização temporal.

### `gene_emergence.py`
Classifica cada gene de resistência identificado como **Ancestral** (presente desde o 
início do dataset) ou **Emergente** (surgiu em um ano específico), respondendo à pergunta 
"quando esse gene de resistência surgiu na população?" — corrigindo o viés de amostragem 
presente na contagem simples por ano.

## Como usar

### Download de genomas por ano
```bash
python download_genomes.py
```
> Requer: `datasets.exe` na pasta do projeto

### Controle de qualidade
```bash
python qc_filter.py
```

## Configuração

O organismo alvo é configurável — o pipeline pode ser aplicado a qualquer 
bactéria com genomas disponíveis no NCBI.

### 22/07 - Adição do módulo `qc_filter.py`

**O que foi feito:**
Adição do módulo `qc_filter.py`, que realiza controle de qualidade sobre os genomas 
baixados pelo `download_genomes.py`. O módulo lê o arquivo `assembly_data_report.jsonl` 
dentro de cada `.zip` e filtra os genomas com base em:

- Nível de montagem: Complete Genome ou Chromosome
- N50 > 50.000 bp
- Tamanho total entre 4,5 MB e 6,5 MB

Genomas corrompidos ou que não atendem os critérios são descartados automaticamente, 
tornando os dados gerados mais confiáveis e alinhados com o princípio de não confiar 
cegamente nos outputs — como recomendado pelo Prof. Steven Salzberg (JHU).

### 26/07 - Adição do módulo `consolidate.py`

**O que foi feito:**
Adição do módulo `consolidate.py` que percorre todos os resultados gerados pelo 
`run_amr_pipeline.py` e consolida a contagem de genes de resistência por ano em 
uma tabela CSV (`amr_longitudinal.csv`).

A tabela gerada tem:
- **Linhas** → anos (2005 → 2025)
- **Colunas** → cada gene de resistência identificado
- **Valores** → quantidade de genomas naquele ano com aquele gene

### 26/07 - Adição do módulo `run_amr_pipeline.py`

**O que foi feito:**
Adição do módulo `run_amr_pipeline.py` que automatiza a execução do BLAST em 
1.977 genomas de *Klebsiella pneumoniae* organizados por ano, gerando um arquivo 
de resultado por genoma em `data/results/`.

**Resultado:**
1.977 análises AMR executadas automaticamente, cobrindo genomas de 2005 a 2025.

### 26/07 - Adição do módulo `dashboard.py` — Pipeline completo!

**O que foi feito:**
Adição do módulo `dashboard.py`, que lê o arquivo `amr_longitudinal.csv` gerado 
pelo `consolidate.py` e gera um dashboard interativo em HTML com a evolução temporal 
dos 10 genes de resistência mais prevalentes em *Klebsiella pneumoniae* (2005-2025).

**Resultado obtido:**
O gráfico revelou padrões biologicamente relevantes:
- Ausência de detecções até 2013 — reflexo do baixo volume de sequenciamento nessa época
- Crescimento acelerado a partir de 2015 — explosão do NGS de baixo custo
- Salto expressivo em 2019-2020 — aumento da vigilância genômica durante a pandemia
- **SHV-100** como gene mais prevalente — consistente com a literatura sobre *K. pneumoniae*

### 28/07 - Normalização e refinamento do pipeline (`consolidate.py` + `dashboard.py`)

**O problema identificado:**
O gráfico original mostrava contagem absoluta de genes por ano, mas isso gerava um viés 
de amostragem: anos com mais genomas sequenciados (ex: 2021 com 581 genomas) naturalmente 
mostravam mais genes do que anos com poucos genomas (ex: 2013 com 8 genomas) — mesmo que 
a resistência real não tivesse aumentado na mesma proporção.

**O que foi feito em `consolidate.py`:**

1. **Contagem única por genoma:** cada gene agora é contado no máximo uma vez por genoma 
   (usando `set()`), corrigindo a distorção causada por múltiplas cópias do mesmo gene 
   aparecendo várias vezes no resultado do BLAST de um único genoma.

2. **Normalização por prevalência:** a contagem de cada gene passou a ser dividida pelo 
   total de genomas daquele ano, convertendo o dado para porcentagem:

   prevalência (%) = (genomas com o gene / total de genomas do ano) × 100

3. **Coluna `total_genomas`:** adicionada ao CSV para permitir filtrar anos com poucos 
   genomas em análises futuras.

**O que foi feito em `dashboard.py`:**

1. **Filtro de anos com baixa amostragem:** anos com menos de 10 genomas são descartados 
   do gráfico, evitando picos artificiais causados por 1-2 genomas isolados.

2. **Seleção por crescimento, não por volume:** os genes exibidos no gráfico principal 
   agora são selecionados pela diferença entre a prevalência média dos 3 primeiros anos 
   e dos 3 últimos anos — destacando genes que realmente emergiram ou aumentaram, e não 
   apenas os mais comuns.

3. **Segundo gráfico (prevalência atual):** adicionado um gráfico complementar com os 
   genes mais prevalentes no último ano disponível. Esse gráfico revelou os genes 
   intrínsecos da espécie (`ArnT`, `LptD`, `OmpA`, `eptB`, `MdtQ`) — genes cromossomais 
   presentes em ~100% dos genomas em todos os anos, distintos dos genes de resistência 
   adquirida via transferência horizontal.

**Resultado:**
O pipeline agora distingue automaticamente entre **genoma core** (genes intrínsecos, 
sempre presentes) e **resistoma acessório** (genes adquiridos, com prevalência variável 
no tempo) — uma distinção biologicamente significativa que serve de base conceitual para 
o próximo módulo, de detecção de emergência de genes.

### 28/07 - Adição do módulo `gene_emergence.py`

**O problema que este módulo resolve:**
O gráfico de evolução temporal mostrava contagem de genes por ano, mas não respondia 
uma pergunta fundamental: **quando cada gene de resistência realmente surgiu na 
população?** Um gene podia aparecer mais em anos recentes simplesmente por haver mais 
genomas sequenciados, não necessariamente porque emergiu naquele período.

**O que foi feito:**
O módulo `gene_emergence.py` percorre o `amr_longitudinal.csv` gene por gene e, para 
cada um, identifica o primeiro ano em que sua prevalência foi maior que zero. Com base 
nisso, classifica cada gene em:

- **Ancestral** — presente desde o primeiro ano do dataset (provavelmente parte do 
  genoma core da espécie ou já disseminado antes do período analisado)
- **Emergente** — ausente no início do dataset e detectado pela primeira vez em um 
  ano específico
- **Nunca detectado** — não encontrado em nenhum genoma analisado

O resultado é salvo em `gene_emergence.csv`, ordenado por ano de emergência.

**Resultado obtido:**
A análise identificou corretamente o surgimento de genes clinicamente relevantes:

- **KPC-2** (carbapenemase) — emergente em **2011**
- **CTX-M-14** (ESBL) — emergente em **2011**

Esses resultados são consistentes com a literatura científica sobre a disseminação 
global desses genes em *Klebsiella pneumoniae* durante a década de 2010, validando 
a abordagem metodológica do pipeline.

**Como usar:**
```bash
python gene_emergence.py
```
> Requer: `amr_longitudinal.csv` gerado pelo `consolidate.py`

### 09/08 - Compatibilidade multiplataforma e checkpoint (Colab)

**O que foi feito:**

O projeto foi portado para rodar no Google Colab, permitindo execução em nuvem 
sem depender do ambiente Windows local. Duas melhorias de código foram necessárias:

1. **`download_genomes.py`** — o script agora detecta o sistema operacional 
   automaticamente (`platform.system()`) e escolhe entre `datasets.exe` (Windows) 
   ou `./datasets` (Linux/Colab), sem precisar de alteração manual.

2. **`run_amr_pipeline.py`** — adicionado sistema de checkpoint: antes de rodar o 
   BLAST em um genoma, o script verifica se o resultado já existe e pula caso 
   positivo. Isso torna o pipeline resiliente a desconexões do Colab, permitindo 
   retomar exatamente de onde parou sem perder progresso ou reprocessar genomas.

**Resultado obtido:**
Pipeline completo executado end-to-end no Colab para *Staphylococcus aureus* 
(2012-2026), confirmando que o projeto funciona de forma genérica para qualquer 
organismo com dados disponíveis no NCBI — não apenas *Klebsiella pneumoniae*.

O gráfico revelou o gene **PC1/blaZ** (penicilinase clássica) como dominante, 
junto com **AAC6_Ie_APH2_Ia** (aminoglicosídeos) e **tet(K)** (tetraciclina), 
todos condizentes com o perfil de resistência conhecido de *S. aureus*. O gene 
**tet(38)**, intrínseco à espécie, apareceu com prevalência constante de 100%.

## Estrutura de dados

data/
├── genomes/
│ └── K_pneumoniae/ ← uma pasta por bactéria
│ ├── raw/ ← zips baixados do NCBI
│ ├── approved/ ← genomas aprovados no QC
│ ├── results/ ← resultados do BLAST por ano
│ └── consolidated/ ← CSV e dashboard final
└── references/
├── card_db/ ← banco BLAST do CARD
└── card-ontology/ ← aro.tsv e arquivos de anotação

> Para adicionar uma nova bactéria, crie uma pasta com o nome dela 
> dentro de `data/genomes/` e siga o mesmo fluxo do pipeline.

## Pipeline completo!

O `amr-longitudinal-pipeline` agora executa o fluxo completo:

download_genomes.py → qc_filter.py → run_amr_pipeline.py → consolidate.py → dashboard.py → gene_emergence.py

Pronto para ser aplicado a qualquer bactéria com genomas disponíveis no NCBI.

## Tecnologias

- Python + Biopython
- BLAST 2.17.0+
- CARD Database 4.0.1
- Pandas — leitura e manipulação do CSV
- Plotly Express — geração do dashboard interativo em HTML
- CheckM (controle de qualidade - implementação futura)
- Nextflow (orquestração — implementação futura)
- Docker (containerização — implementação futura)

## Status

🚧 Em desenvolvimento