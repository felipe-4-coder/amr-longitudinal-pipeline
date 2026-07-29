import pandas as pd
import plotly.express as px

def gerar_dashboard():
    csv_path = input("Digite o caminho do arquivo CSV: ")

    # Lê o CSV
    df = pd.read_csv(csv_path, index_col="ano")

    # Seleciona os 10 genes mais prevalentes no total
    top_genes = df.sum().nlargest(10).index.tolist()
    df_top = df[top_genes]

    # Gera o gráfico

    organismo = input("Digite o nome do organismo (ex: Klebsiella pneumoniae): ")
    anos = df.index.min(), df.index.max()

    fig = px.line(

        df_top.reset_index(),
        x="ano",
        y=top_genes,
        title=f"Evolução da Resistência Antimicrobiana em {organismo} ({anos[0]} - {anos[1]})", 
        labels={"value": "Número de genomas", "ano": "Ano", "variable": "Gene"}
    )

    # Salva como HTML interativo
    output_html = input("Digite o caminho para salvar o dashboard (ex: data/dashboard.html): ")
    fig.write_html(output_html)
    print(f"Dashboard salvo em: {output_html}")

gerar_dashboard()