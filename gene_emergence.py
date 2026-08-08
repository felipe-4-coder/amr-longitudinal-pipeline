import pandas as pd

def gene_emergence():

    # Digite o caminho contendo os arquivos a serem analisados
    csv_path = input("Digite o caminho do arquivo CSV: \n")

    # Digite o diretório de saida para o resultado da análise
    output_dir = input("Digite o diretório de saída para os resultados: \n")

    df = pd.read_csv(csv_path, index_col="ano")
    resultados = []
    primeiro_ano_dataset = df.index.min()
    anos_ordenados = sorted(df.index.tolist())

    for gene in df.columns:

        serie_do_gene = df[gene]  # pega a coluna inteira
        anos_com_gene = serie_do_gene[serie_do_gene > 0].index.tolist()

        if anos_com_gene:
            candidato = anos_com_gene[0]

            # pega a posição do candidato na lista de anos ordenados
            posicao = anos_ordenados.index(candidato)
            proximos_3_anos = anos_ordenados[posicao+1 : posicao+4]

            # conta em quantos desses anos o gene também apareceu
            persistiu = sum(1 for ano_seguinte in proximos_3_anos if ano_seguinte in anos_com_gene)

            if persistiu >= 2:
                ano_emergencia = candidato
            else:
                ano_emergencia = None
        else:
            ano_emergencia = None

        if ano_emergencia == primeiro_ano_dataset:
            status = "Ancestral"
        elif ano_emergencia is None:
            status = "Nunca detectado / não persistiu"
        else:
            status = "Emergente"

        resultados.append({
            "gene": gene,
            "ano_emergencia": ano_emergencia,
            "status": status
        })

    df_resultado = pd.DataFrame(resultados)
    df_resultado = df_resultado.sort_values("ano_emergencia")

    output_path = f"{output_dir}/gene_emergence.csv"
    df_resultado.to_csv(output_path, index=False)

    print(f"Resultado salvo em: {output_path}")

gene_emergence()