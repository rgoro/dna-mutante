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
Se implementó una API para exponer este test de ADN mutante al público.  Para eso se usó *Flask*, un *microframework* para desarrollo web en Python.  La interfaz de la API es la siguiente:

* `/mutant` -- POST para determinar si una secuencia de adn corresponde a un mutante o no 
  + Recibe un JSON según el formato que se especifica más adelante
  + Respuestas posibles:
    * HTTP 200 Si el ADN es mutante, junto con un json de salida válida (ver más abajo)
    * HTTP 403 Si el ADN no es mutante, junto con un json de salida válida (ver más abajo)
    * HTTP 400 Si la secuencia de entrada es inválida, junto con un json de salida erróneo (ver más abajo)
    * HTTP 500 Si se produce otro tipo de error, junto con un json de salida erróneo (ver más abajo)

#### JSONs de entrada
El json de entrada es:

```javascript
{
	"dna" : secuencia
}
```

Donde `secuencia` es un array de strings según el formato esperado por el problema (N strings de largo N; sólo las letras 'a', 't', 'c' y 'g')

#### JSONs de salida
En una salida válida el POST devuelve un json con el formato

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


