#!/usr/bin/env python3

# Script Python para procesar la lista de consultas y generar listas de documentos
# potencialmente relevantes para las mismas. Este código será el que genere las
# denominadas runs que se le pasarían a ranx junto con los juicios de relevancia para el
# cálculo de las métricas de rendimiento. 
# **Hasta 1,5 puntos.**

from elasticsearch import Elasticsearch
import json
from datetime import datetime

def main():
    
    inicio = datetime.now()
    
    # Configuración de la conexión con el servidor de Elasticsearch
    #
    ELASTIC_HOST = "https://localhost:9200"
    ELASTIC_CERT = "content/http_ca.crt"
    ELASTIC_USER = "elastic"
    ELASTIC_PASSWORD = "dKPZ*UTCUQKn83cfR8vw"

    # Conectar al servidor de Elasticsearch
    #
    es = Elasticsearch(
        ELASTIC_HOST, ca_certs=ELASTIC_CERT, basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
    )

    # Carga de consultas desde archivo CISI.QRY
    #
    with open("content/cisi/CISI.QRY", "rt") as file:
        queries = file.read().split(".I ")

    # Procesamiento de consultas y creación de runs
    #
    run_results = []
    for query in queries[1:]:  # Ignorar el primer elemento vacío
        query_id = query.splitlines()[0]
        query_text = parse_query(query)

        # Realizar la búsqueda en Elasticsearch
        #
        results = es.search(
            index="cisi",
            query={
                "match": {
                    "text": query_text
                }
            },
            size=100
        )
        
        documents = results['hits']['hits']
        
        # Recolectar los IDs de los documentos para el run
        #
        for doc in documents:
            run_results.append({
                "query_id": query_id,
                "doc_id": doc["_id"],
                "score": doc["_score"]
            })

    # Guardar los resultados en un archivo JSON
    #
    with open("runs.json", "w") as outfile:
        json.dump(run_results, outfile, indent=4)
        
    fin = datetime.now()
    
    print(fin - inicio)

def parse_query(query_text):
    lines = query_text.splitlines()
    query_content = ""
    for line in lines:
        if line.startswith('.W'):
            query_content += " ".join(lines[lines.index(line)+1:])
            break
    return query_content.strip()

if __name__ == "__main__":
    main()