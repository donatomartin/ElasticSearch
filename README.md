
# ElasticSearch

Repo del proyecto para el curso de Repositorios de Información (RI) de la Universidad de Oviedo.

[Enunciado del proyecto](https://www.campusvirtual.uniovi.es/pluginfile.php/530084/mod_resource/content/1/ElasticSearch%20Evaluaci%C3%B3n%20Extraordinaria%202024.pdf)

[Ver documentación](doc.md)

## Parámetros del proyecto

- Colección de pruebas: CISI
- No se deben eliminar palabras vacías
- Se debe aplicar stemming
- No se debe usar shingles
- Métricas: Bpref y Hits

## Colección de pruebas

```python
print(288787 % 6) # 1
```

0. CACM
1. **CISI**
2. Cranfield
3. LISA
4. Medline
5. NPL

[Enlace a la colección](https://ir.dcs.gla.ac.uk/resources/test_collections/cisi/)

## Configuración del índice

```python
print(28878 % 2) # 0
```

0. **No tienes que eliminar palabras vacías.**
1. Tienes que eliminar palabras vacías.

```python
print(2887 % 2) # 1
```

0. No tienes que aplicar stemming.
1. **Tienes que aplicar stemming.**

```python
print(288 % 2) # 0
```

0. **No tienes que usar shingles.**
1. Tienes que usar shingles.

## Métricas

```python
print(288787 % 12) # 7
print((288787 % 12 + 6) % 12) # 1
```

1. **Hits**
2. Hit Rate
3. Precision
4. Recall
5. F1
6. r-Precision
7. **Bpref**
8. Rank-biased Precision (RBP)
9. Mean Reciprocal Rank (MRR)
10. Mean Average Precision (MAP)
11. Discounted Cumulative Gain (DCG)
12. Normalized Discounted Cumulative Gain (NDCG)