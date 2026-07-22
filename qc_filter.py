import os
import zipfile
import json

def qc_filter():

    data_dir = input("Digite o caminho da pasta com os arquivos .zip: ")
    approved_dir = input("Digite o caminho da pasta de saída para genomas aprovados: ")

    os.makedirs(approved_dir, exist_ok=True)

    for arquivo in os.listdir(data_dir):
        if arquivo.endswith(".zip"):
            print(arquivo)
            caminho_zip = os.path.join(data_dir, arquivo)
        
            try:
                with zipfile.ZipFile(caminho_zip, "r") as z:
                    with z.open("ncbi_dataset/data/assembly_data_report.jsonl") as f:
                        conteudo = f.read()
                        for linha in conteudo.decode("utf-8").splitlines():
                            dados = json.loads(linha)
                            nivel = dados.get("assemblyInfo", {}).get("assemblyLevel", "")
                            n50 = dados.get("assemblyStats", {}).get("contigN50", 0)
                            tamanho = int(dados.get("assemblyStats", {}).get("totalSequenceLength", 0))
                            if nivel in ["Complete Genome", "Chromosome"] and n50 > 50000 and 4500000 < tamanho < 6500000:
                                print(f"  ✓ APROVADO: {dados.get('accession', 'N/A')}")
                            else:
                                print(f"  ✗ REPROVADO: {dados.get('accession', 'N/A')}")
            except zipfile.BadZipFile:
                print(f"  ⚠ CORROMPIDO: {arquivo} — pulando")

qc_filter()