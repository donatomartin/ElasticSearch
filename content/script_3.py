#!/usr/bin/env python3

# Script Python que utilice ranx, reciba las runs generadas por el script anterior y
# sea capaz de procesar los juicios de relevancia para evaluar el
# rendimiento del buscador según las dos métricas que le corresponda utilizar al estudiante.
# **Hasta 2,5 puntos.**

import json

def read_runs():
    with open("runs.json", 'r') as file:
        runs = json.load(file)
    return runs

def read_relevance():
    relevance = {}
    with open("content/cisi/CISI.REL", 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            query_id = parts[0]
            doc_id = parts[1]
            if query_id not in relevance:
                relevance[query_id] = set()
            relevance[query_id].add(doc_id)
    return relevance

def calculate_bpref(runs, relevance):
    bpref_scores = {}
    for query_id in relevance:
        relevant_docs = relevance[query_id]
        non_relevant_seen = 0
        relevant_retrieved_before_first_non_relevant = 0
        total_relevant = len(relevant_docs)
        
        for run in [r for r in runs if r['query_id'] == query_id]:
            if run['doc_id'] in relevant_docs:
                relevant_retrieved_before_first_non_relevant += 1 - (non_relevant_seen / total_relevant)
            else:
                non_relevant_seen += 1
        
        if total_relevant > 0:
            bpref_scores[query_id] = relevant_retrieved_before_first_non_relevant / total_relevant
        else:
            bpref_scores[query_id] = 0

    return bpref_scores

# Lee de los ficheros
#
runs = read_runs()
relevance = read_relevance()

# Calcula las métricas
#
bpref_scores = calculate_bpref(runs, relevance)

# Muestra los resultados
#
print("Bpref Scores:", bpref_scores)
