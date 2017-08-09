# Test de DNA Mutante

Esta es una solución al problema de detectar si una secuencia de ADN corresponde a un mutante o no.  El ADN se presenta como una lista de N strings de N caracteres, que sólo pueden ser 'a', 't', 'c' y 'g', y se considera mutante cuando hay una secuencia de cuatro caracteres iguales, en horizontal, vertical o diagonal.

La implementación se realizó en *Python* 2.7 y para la API web se usó *Flask*.


## Manual de uso
### Línea de comandos
El script con el código para definir si una secuencia de ADN es mutante está en el archivo `adm_mutante.py`, pero no se implementó *I/O* como para hacer consultas directamente.  Para testearlo existe un archivo con tests de unidad: `test_adn_mutante.py`, que usa el módulo *unittest*, estándard de Python.  Para ejecutar la batería de tests correr:

```
$ python -m unittest test_adn_mutante.TestADNMutante
```

O, para ejecutar un test en particular:

```
$ python -m unittest test_adn_mutante.TestADNMutante.<nombre_del_test>
```

#### Tests implementados
Se implementaron los siguientes tests:

* Los dos ejemplos del enunciado.
* Cuatro pares de tests con dos secuencias en cada dirección.
* Un test para confirmar que si hay una secuencia de más de 4 caracteres se cuenta como una sola.
* Un test para verificar que no hay diferencia con mayúsculas y minúsculas en las secuencias.
* Un test para confirmar que ante caracteres extraños se lanza una excepción.
* Tres test para matrices de distintos tamaños (N = 5 y N = 4).
* Un test para confirmar que no se analizan tablas de tamaño inferior a 4.
* Un test para confirmar que ante un string de tamaño diferente a N se lanza una excepción.

### API
Se implementó una API para exponer este test de ADN mutante al público.  Para eso se usó *Flask*, un *microframework* para desarrollo web en Python. La API se puede testear en http://ec2-54-175-60-181.compute-1.amazonaws.com:5000/ . En esta versión deployada están cargados los dos ejemplos del enunciado.

La interfaz de la API es la siguiente:

* [/mutant](http://ec2-54-175-60-181.compute-1.amazonaws.com:5000/mutant) -- POST para determinar si una secuencia de adn corresponde a un mutante o no 
  + Recibe un JSON según el formato que se especifica más adelante
  + Respuestas posibles:
    * HTTP 200 Si el ADN es mutante, junto con un JSON de salida válida (ver más abajo)
    * HTTP 403 Si el ADN no es mutante, junto con un JSON de salida válida (ver más abajo)
    * HTTP 400 Si la secuencia de entrada es inválida, junto con un JSON de salida erróneo (ver más abajo)
    * HTTP 500 Si se produce otro tipo de error, junto con un JSON de salida erróneo (ver más abajo)
* [/stats](http://ec2-54-175-60-181.compute-1.amazonaws.com:5000/stats) -- GET para obtener las estadísticas de los ADNs registrados
  + Responde con un JSON según el formato especificado más abajo

#### JSONs de entrada
El JSON de entrada es:

```javascript
{
	"dna" : secuencia
}
```

Donde `secuencia` es un array de strings según el formato esperado por el problema (N strings de largo N; sólo las letras 'a', 't', 'c' y 'g')

#### JSONs de salida

##### Para `/mutant`
En una salida válida el POST devuelve un JSON con el formato

```javascript
{
	"esMutante" : bool
}
```

En caso de error devuelve 
```javascript
{
	"error_text" : string
}
```

##### Para `/stats`
Devuelve un JSON con el siguiente formato.

```javascript
{
  "count_human_dna": int, 
  "count_mutant_dna": int, 
  "ratio": float
}
```

## Detalles de implementación

### Algoritmo
El chequeo de la secuencia de ADN se hace recorriendo la tabla una sola vez.  Esto permite cierta eficiencia en la verificación (el órden de complejidad del algoritmo es *O(n²)*, donde *n* es el largo de cada cadena de ADN (que es igual al alto de la tabla).  Como contrapartida, se pierde cierta legibilidad del código ya que se hace necesario mantener al mismo tiempo el estado de las potenciales secuencias en las verticales y en las diagonales.  Para esto se usó una tupla `<ultima_letra, largo_secuencia>` (LS) y se mantienen tres listas, `verticales` (V), `diag_izq_der` (DID) y `diag_der_izq` (DDI).

`V[j]` contiene la información para la columna *j* de la tabla de ADN.  Para identificar a las diagonales, se aprovechó que las listas de Python se pueden indexar con números negativos.  DID[i - j] mantiene la información de la diagonal que empieza en ADN<sub>ij</sub>, es decir, la principal está en DID[0], la inmediata inferior en DID[-1], la inmediata superior en DID[1], etc.  Para DDI la cuenta resultó un poco más incómoda de leer: DDI[i + j - N] contiene los datos de la diagonal que empieza en ADN<sub>ij</sub>, por lo que la diagonal principal en este sentido, que empieza en ADN<sub>(N-1)(N-1)</sub> está en DDI[-1], la inmediata inferior en DDI[0], la inmediata superior en DDI[-2], etc.

La operatoria con esta información es siempre la misma.  Para cada caracter de cada *string* se compara con la letra anterior para las secuencias horizontales y con la información correspondiente en V, DID y DDI, si corresponde.  Si es la misma letra, se aumenta en 1 el largo de secuencia, si no se pone en 1 y se reemplaza la letra.  Cuando un largo de secuencia en cualquiera de estas direcciones alcanza 4 se anota que hay una secuencia potencialmente mutante y, ni bien se detectan 2, se devuelve `True`.

### API
La API está implementada de la forma más sencilla posible, y servida directamente desde Python.  No se implementó ningún tipo de resguardo de carga ya que, para evaluar y testear correctamente los requerimientos de capacidad de carga es necesario ejecutar una serie de tests de costo (en tiempo y valor) excesivo para este ejercicio.  Opciones a considerar si se quisiera deployar la aplicación "de verdad" incluyen:

* **AWS Elastic Beanstalk** Es un entorno de depoyment propio de amazon para hostear aplicaciones, independientemente de la tecnología de implementación.  Brinda todas las herramientas propias de monitoreo y balanceo de carga de amazon, pero acopla la aplicación al entorno productivo.
* **NGINX** u otro servidor web liviano.  Esta es la solución más flexible, pero con mayor carga de configuración del lado del equipo de desarrollo/devOps.  Se propone nginx por contar con experiencia con la herramienta, pero asimismo se podría usar lighthttpd. No se recomienda usar Apache si se busca un entorno liviano y rápido.

Independientemente del hosting elegido, sería necesaria alguna solución de cache para reducir los requests sobre el servidor.  Se puede usar *Varnish* o alguna herramienta similar en un servidor aparte.


Se eligió Amazon Web Services como solución de hosting dado a que ya se contaba con cierta experiencia en dicho ambiente.  Se eligió como base de datos *DynamoDB*, base de datos *NoSQL* propia de Amazon, por ser donde se estaba deployando el trabajo.  No se optó por una solución SQL debido a que se consideró que la sencillez de los datos no merecía más complejidad.

### Base de datos
Los ADNs consultados se guardan en la base de datos identificándolos con un hash de la secuencia, concatenando todos los strings de la tabla.  En esta implementación se optó por tomar los primeros 10 dígitos de un *SHA1* de este string, dado que el hash completo resulta un número demasiado grande para usar de identificador en la base de datos.  Por supuesto esta opción no es la mejor, dado que tomar una parte del hash es vulnerable a las colisiones.  En una solución productiva podría ser conveniente buscar otra función de hash o bien desarrollar una propia, teniendo en cuenta que las cadenas tienen sólo 4 caracteres posibles.

Hay un mínimo test de unidad para el acceso a la base de datos, `test_adn_db.py`, que se puede correr teniendo una copia local de DynamoDB (ver http://docs.aws.amazon.com/amazondynamodb/latest/gettingstartedguide/Welcome.html para instrucciones de instalación).
