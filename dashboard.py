import pandas as pd
import plotly.express as px

def gerar_dashboard():
    csv_path = input("Digite o caminho do arquivo CSV: ")

    # Lê o CSV
    df = pd.read_csv(csv_path, index_col="ano")
    df = df[df["total_genomas"] >= 10]  # filtra anos com poucos genomas
    df = df.drop(columns=["total_genomas"])  # remove a coluna antes de plotar

    # Seleciona os 10 genes mais prevalentes no total
    # seleciona genes com maior variação ao longo do tempo
    anos_ordenados = sorted(df.index)
    primeiros_anos = anos_ordenados[:3]
    ultimos_anos = anos_ordenados[-3:]

    media_inicial = df.loc[primeiros_anos].mean()
    media_final = df.loc[ultimos_anos].mean()

    crescimento = media_final - media_inicial
    top_genes = crescimento.nlargest(10).index.tolist()
    df_top = df[top_genes]

    # Gera o gráfico

    organismo = input("Digite o nome do organismo (ex: Klebsiella pneumoniae): ")
    anos = df.index.min(), df.index.max()

    fig = px.line(

        df_top.reset_index(),
        x="ano",
        y=top_genes,
        title=f"Evolução da Resistência Antimicrobiana em {organismo} ({anos[0]} - {anos[1]})", 
        labels={"value": "Prevalência (%)", "ano": "Ano", "variable": "Gene"}

    )

    # Segundo gráfico: Top prevalência no último ano
    ultimo_ano = anos_ordenados[-1]
    top_prevalencia = df.loc[ultimo_ano].nlargest(10).index.tolist()
    df_prevalencia = df[top_prevalencia]

    fig2 = px.line( 
        df_prevalencia.reset_index(),
        x="ano",
        y=top_prevalencia,
        title=f"Genes Mais Prevalentes Atualmente em {organismo} ({ultimo_ano})",
        labels={"value": "Prevalência (%)", "ano": "Ano", "variable": "Gene"}

    )

    # Salva como HTML interativo
    output_html = input("Digite o caminho para salvar o dashboard (ex: data/dashboard.html): ")
    fig.write_html(output_html)

    output_html2 = output_html.replace(".html", "_prevalencia.html")
    fig2.write_html(output_html2)

    print(f"Dashboard salvo em: {output_html} e {output_html2}")

gerar_dashboard()