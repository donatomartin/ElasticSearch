#!/usr/bin/env python3

# Script Python para procesar la colección de documentos y crear el índice en ElasticSearch.
# **Hasta 1,5 puntos.**
#

# Parámetros:
# - Colección de pruebas: CISI
# - No se deben eliminar palabras vacías
# - Se debe aplicar stemming
# - No se debe usar shingles
#

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from datetime import datetime

def main():

    inicio = datetime.now()
    
    global es

    # Configuración de la conexión con el servidor de Elasticsearch
    #
    ELASTIC_HOST = "https://localhost:9200"
    ELASTIC_CERT = "content/http_ca.crt"
    ELASTIC_USER = "elastic"
    ELASTIC_PASSWORD = "dKPZ*UTCUQKn83cfR8vw"

    # Conectar al servidor
    #
    es = Elasticsearch(
        ELASTIC_HOST, ca_certs=ELASTIC_CERT, basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
    )

    # Crear el índice
    #
    # Si no se crea explícitamente se crea al indexar el primer documento
    #
    # Debemos crearlo puesto que el mapeado por defecto (mapping) de algunos
    # campos, no es satisfactorio.
    #
    # ignore=400 hace que se ignore el error de índice ya existente
    #
    args = {
        "settings": {
            "analysis": {
                "filter": {
                    "estematizacion_ingles": {"type": "stemmer", "name": "porter2"},
                },
                "analyzer": {
                    "analizador_personalizado": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "estematizacion_ingles"],
                    },
                    "analizador_autores": {
                        "tokenizer": "standard",
                        "filter": ["lowercase"]
                    }
                },
            }
        },
        "mappings": {
            "properties": {
                "text": {
                    "type": "text",
                    "analyzer": "analizador_personalizado",
                    "fielddata": "true",
                },
                "author": {
                    "type": "text",
                    "analyzer": "analizador_autores",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
            }
        },
    }

    es.indices.create(index="cisi", ignore=400, body=args)

    # Indexar los documentos
    # Leemos el fichero completo y lo procesamos
    #
    global contador
    contador = 0

    with open("content/cisi/CISI.ALL", "rt") as file:
        
        content = file.read()

        parse_documents(content)


    fin = datetime.now()

    print(fin - inicio)

# Parsear los documentos
#
def parse_documents(content):
    
    entries = content.split('.I ')[1:] # Ignorar el primer documento vacío

    documents = []
    for entry in entries:
        doc = {
            "_index": "cisi",
            "_id": entry.splitlines()[0],
        }

        lines = entry.splitlines()
        current_section = None

        for line in lines:

            if line.startswith('.T'): 
                current_section = 'text'
                continue
            elif line.startswith('.W'):
                current_section = 'text'
                continue
            elif line.startswith('.B'):
                current_section = 'text'
                continue
            elif line.startswith('.A'):
                current_section = 'author'
                continue
            elif line.startswith('.X'):
                current_section = None
                continue
    
            if current_section:
                doc[current_section] = doc.get(current_section, "") + line.strip() + " "

        # Mostrar los documentos por pantalla
        #
        # print(doc + "\n\n")
        
        documents.append(doc)

    helpers.bulk(es, documents, chunk_size=len(documents))

if __name__ == "__main__":
    main()
