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

## Tecnologias

- Python + Biopython
- BLAST 2.17.0+
- CARD Database 4.0.1
- CheckM (controle de qualidade)
- Nextflow (orquestração — implementação futura)
- Docker (containerização — implementação futura)

## Status

🚧 Em desenvolvimento