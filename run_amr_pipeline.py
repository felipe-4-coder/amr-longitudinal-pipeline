import subprocess
import os

def amr_search_tool():

    # Solicita o caminho da pasta com os genomas a serem analisados.
    genomes_folder = input("Digite o caminho da pasta contendo os genomas a serem analisados: ")

    # Solicita o banco de dados que será usado para realizar a comparação e busca de genes de resistência.
    amr_database = input("Digite o caminho do banco de dados AMR (Antimicrobial Resistance): ")

    # Solicita o caminho de saida para o resultado da análise dos genomas.
    output_dir = input("Digite o caminho de saida para o resultado da análise: ")

    for ano in os.listdir(genomes_folder):
        pasta_ano = os.path.join(genomes_folder, ano, "ncbi_dataset", "data")

        if not os.path.exists(pasta_ano):
            continue

        for genoma in os.listdir(pasta_ano):

            print(f"Analisando {ano}/{genoma}...")

            pasta_genoma = os.path.join(pasta_ano, genoma)

            for arquivo in os.listdir(pasta_genoma):
                if arquivo.endswith(".fna"):
                    fna_path = os.path.join(pasta_genoma, arquivo)

            resultado_path = os.path.join(output_dir, ano, f"{genoma}.txt")
            os.makedirs(os.path.join(output_dir, ano), exist_ok=True)

            # Executa o comando para realizar a busca de genes de resistência a antimicrobianos.
            
            subprocess.run([
                "blastn", "-query", fna_path,
                "-db", amr_database,
                "-out", resultado_path,
                "-outfmt", "6",
                "-perc_identity", "90"
            ])

amr_search_tool()