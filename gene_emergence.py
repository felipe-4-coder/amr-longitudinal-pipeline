import pandas as pd

def gene_emergence():

    # Digite o caminho contendo os arquivos a serem analisados
    csv_path = input("Digite o caminho do arquivo CSV: \n")

    # Digite o diretório de saida para o resultado da análise
    output_dir = input("Digite o diretório de saída para os resultados: \n")

    df = pd.read_csv(csv_path, index_col="ano")
    resultados = []
    primeiro_ano_dataset = df.index.min()

    for gene in df.columns:

        serie_do_gene = df[gene] # pega a coluna inteira
        anos_com_gene = serie_do_gene[serie_do_gene > 0].index.tolist()

        if anos_com_gene:
            ano_emergencia = anos_com_gene[0]
        else:
            ano_emergencia = None # gene nunca apareceu

        if ano_emergencia == primeiro_ano_dataset:
            status = "Ancestral"
        elif ano_emergencia is None:
            status = "Nunca detectado"
        else:
            status = "Emergente"

        resultados.append({
            "gene": gene,
            "ano_emergencia": ano_emergencia,
            "status": status
        })

    df_resultado = pd.DataFrame(resultados )
    df_resultado = df_resultado.sort_values("ano_emergencia")

    output_path = f"{output_dir}/gene_emergence.csv"
    df_resultado.to_csv(output_path, index=False)

    print(f"Resultado salvo em: {output_path}")

gene_emergence()
