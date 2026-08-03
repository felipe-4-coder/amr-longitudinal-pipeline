import os
import csv

def func_longitudinal():

    # Indica o diretório dos arquivos contendo os genomas
    results_dir = input("Digite o caminho do diretório contendo so resultados: ")

    # Indica o diretório para a saida do resultados
    output_dir = input("Digite o caminho para o resultado da análise: ")

    contagem = {}  # {ano: {gene: contagem}}
    total_genomas = {}

    for ano in os.listdir(results_dir):
        pasta_ano = os.path.join(results_dir, ano)
    
        for arquivo in os.listdir(pasta_ano):
            if arquivo.endswith(".txt"):
                
                if ano not in total_genomas:
                    total_genomas[ano] = 0
                total_genomas[ano] += 1

                caminho_txt = os.path.join(pasta_ano, arquivo)
                genes_no_genoma = set()
                with open(caminho_txt, "r") as f:
                    for linha in f:
                        columns = linha.strip().split('\t')
                        if len(columns) >= 2:
                            gene = columns[1].split('|')[-1]
                            genes_no_genoma.add(gene)

                if ano not in contagem:
                    contagem[ano] = {}
                for gene in genes_no_genoma:
                    if gene not in contagem[ano]:
                        contagem[ano][gene] = 0
                    contagem[ano][gene] += 1

    # após o for ano (fora dele, mesmo nível que contagem = {})
    csv_path = os.path.join(output_dir, "amr_longitudinal.csv")
    os.makedirs(output_dir, exist_ok=True)

    # pega todos os genes únicos encontrados
    todos_genes = sorted(set(g for genes in contagem.values() for g in genes))

    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ano", "total_genomas"] + todos_genes)

        for ano in sorted(contagem.keys()):
            total = total_genomas.get(ano, 1)
            linha = [ano, total] + [round(contagem[ano].get(gene, 0) / total * 100, 2) for gene in todos_genes]
            writer.writerow(linha)
            

    print(f"Resultado salvo em: {csv_path}")

func_longitudinal()