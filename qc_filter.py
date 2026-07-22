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

            ano = arquivo.replace(".zip", "").split("_")[-1]
            pasta_ano = os.path.join(approved_dir, ano)
            os.makedirs(pasta_ano, exist_ok=True)
        
            try:
                with zipfile.ZipFile(caminho_zip, "r") as z:
                    with z.open("ncbi_dataset/data/assembly_data_report.jsonl") as f:

                        conteudo = f.read()

                        aprovados = set()

                        for linha in conteudo.decode("utf-8").splitlines():
                            dados = json.loads(linha)
                            accession = dados.get("accession", "")
    
                            # pula se já processou esse accession
                            if accession in aprovados:
                                continue
    
                            nivel = dados.get("assemblyInfo", {}).get("assemblyLevel", "")
                            n50 = dados.get("assemblyStats", {}).get("contigN50", 0)
                            tamanho = int(dados.get("assemblyStats", {}).get("totalSequenceLength", 0))
    
                            if nivel in ["Complete Genome", "Chromosome"] and n50 > 50000 and 4500000 < tamanho < 6500000:
                                aprovados.add(accession)
                            # extrai FASTA...

                            for nome_arquivo in z.namelist():
                                if accession in nome_arquivo and nome_arquivo.endswith(".fna"):
                                    z.extract(nome_arquivo, pasta_ano)
                                    print(f"  ✓ APROVADO e extraído: {accession}")
                            else:
                                print(f"  ✗ REPROVADO: {dados.get('accession', 'N/A')}")
            except zipfile.BadZipFile:
                print(f"  ⚠ CORROMPIDO: {arquivo} — pulando")

qc_filter()