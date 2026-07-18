import subprocess

def download_genomes():

    # Solicita ao usuário o nome do organismo
    org_assembly = input("Digite o nome do organismo que deseja baixar o genoma: ")

    # Solicita ao usuário o diretório de saída para salvar os genomas
    output_dir = input("Digite o diretório de saída para salvar os genomas: ")

    # Loop para baixar os genomas de 2000 a 2026
    for ano in range(2000, 2027):
        subprocess.run([
            "datasets.exe",
            "download", "genome", "taxon", org_assembly,
            "--assembly-source", "RefSeq",
            "--assembly-level", "complete",
            "--released-after", f"{ano}-01-01",
            "--released-before", f"{ano}-12-31",
            "--filename", f"{output_dir}/{org_assembly}_{ano}.zip"
            ])

download_genomes()