
# ElasticSearch - Documentación de la práctica

> Se detalla a continuación documentaciones de los 3 scripts contenidos en este mismo directorio. Los enunciados tanto del script como de la propia tarea de descripción y muestreo están incluídos en cada una de las siguientes partes.

- Donato A. Martín ( UO288787@uniovi.es )
- Repositorios de Información, Universidad de Oviedo
- 2024

# Primera parte

Documentación correspondiente a esta fase señalando al menos las decisiones tomadas en relación con los documentos (p.ej., si se decidió ignorar alguna sección de los mismos), su preprocesamiento (p.ej., decisiones sobre el algoritmo de stemming, el tamaño de los shingles, el paso a minúsculas, etc.) así como comentarios (y enlaces) sobre la utilidad (o no) del uso de ChatGPT para resolver esta tarea.
**Hasta 1 punto.**

![portada para la parte 1](imgs/image.png)

## Enunciado del script

Script Python para procesar la colección de documentos y crear el índice en ElasticSearch.
**Hasta 1,5 puntos.**

## Contenido

Para la realización de este ejercicio lo primero que debemos hacer es entender cómo se organiza y qué en qué consiste realmente la colección CISI, para ello se deberá leer el enunciado de la práctica y hacer un par de búsquedas rápidas en internet.

Una vez hecho este pequeño research podemos determinar que CISI.ALL es un fichero muy utilizado en el campo de la recuperación de información que contiene 1.460 textos en una notación que incluye campos como identificador, título o resumen.

Cada entrada sigue el siguiente formato:

```
.I <ID>
.T <Título>
.W <Resumen>
.B <Año de publicación del artículo>
.A <Lista de autores>
.X <Lista de referencias cruzadas a otros documentos>
```

Cuando ya es conocido nuestro objetivo, el siguiente paso es determinar qué información nos es relevante para parsear e indexar en nuestro elastic. Un poco en línea con el enunciado de la práctica podemos acordar que las referencias cruzadas no iban a aportar nada en lo que a recuperación de información se refiere ya que no nos muestran información relevante sobre la temática del documento, es por ello que el campo X no será indexado.

El resto; id, título, resúmen, fecha y autores, todo ello nos permitiría localizar el documento por aportar información directamente relacionada con el mismo. Parsearlo ha supuesto un reto mayor del que me esperaba, pese a no ser demasiado complicado, la estructuración en secciones dificulta la lectura por líneas al tener que guardar un contexto de la sección en la que te encuentras y si esta pertenece o no a un nuevo documento. En cualquier caso con este heurístico el trabajo fue realizado correctamente:

```python
for line in lines:

    if line.startswith('.T'):
        current_section = 'title'
    elif line.startswith('.W'):
        current_section = 'text'
    elif line.startswith('.B'):
        current_section = 'created_at'
    elif line.startswith('.A'):
        current_section = 'author'
    elif line.startswith('.X'):
        current_section = None
    
    if current_section:
        doc[current_section] = doc.get(current_section, "") + line.strip() + " "
```

Consideramos X e I secciones nulas pues I nos permite dividir todo el fichero en las diferentes entradas y X no tiene ser indexado como propósito. Más allá de eso simplemente se añade a un diccionario cada una de las líneas en función de la sección en la que nos encontremos, si la sección es nula, será ignorada.

# Segunda parte

Documentación correspondiente a esta fase señalando al menos las decisiones tomadas en relación a la creación de las listas de documentos relevantes. Téngase en cuenta que son colecciones pequeñas y que ElasticSearch puede generar listas de resultados de hasta 10.000 documentos. No hay ningún problema en ello pero dependiendo de cuántos documentos se retornen se obtendrán unas medidas de rendimiento u otras y pueden arrojar luz sobre la percepción que tendría un usuario final del buscador.
**Hasta 1 punto.**

![portada para la parte 2](imgs/image-1.png)

## Enunciado del script

Script Python para procesar la lista de consultas y generar listas de documentos potencialmente relevantes para las mismas. Este código será el que genere las denominadas runs que se le pasarían a ranx junto con los juicios de relevancia para el cálculo de las métricas de rendimiento. 
**Hasta 1,5 puntos.**

## Contenido

# Tercera parte

Documentación correspondiente a esta fase señalando al menos las decisiones tomadas en relación al procesamiento de los juicios de relevancia así como la interpretación de los resultados de la evaluación, las posibles causas para los mismos y las implicaciones para un usuario final.
**Hasta 2,5 puntos.**

![portada para la parte 3](imgs/image-2.png)

## Enunciado del script

Script Python que utilice ranx, reciba las runs generadas por el script anterior y sea capaz de procesar los juicios de relevancia para evaluar el rendimiento del buscador según las dos métricas que le corresponda utilizar al estudiante.
**Hasta 2,5 puntos.**

## Contenido
