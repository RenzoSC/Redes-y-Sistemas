# Informe del Laboratorio 3 - Transporte

## Integrantes:

* Renzo Condormango
* Simón Celoria
* Francisco Porcel de Peralta

## Introducción:
En este laboratorio tuvimos que simular como se comportaba una red en base a diferentes escenarios. Primero empezamos con 
una red simple que solo intentaba pasar paquetes de un punto a otro sin tener en cuenta que se podía producir un cuello de 
botella. En base a los dos casos que nos dieron y los datarate que tenían las distintas conexiones, el cuello de botella se
podía producir en un punto u otro. Finalmente tuvimos que desarrollar más nuestra red para poder solucionar estos problemas
de **_control de flujo_** y **_control de congestión_**

## Herramientas:
Para la realización de este laboratorio utilizamos el software de OMNNET++ para poder simular las redes. 

Usamos C++ para la codificación de los distintos componentes de una red y Python junto con Jupyter Notebook para la 
visualización de los distintos gráficos de los escenarios.

# Red simple:
La red simple está conformada por un **nodo transmisor** `nodeTx`, un **nodo receptor** `nodeRx` y un nodo intermedio que
conecta los dos nodos anteriores simulando una subred.

-imagen-

### Esta red esta desarrollada de la siguiente manera:
* El `nodeTx` genera paquetes de 12500 bytes, estos son generados cada cierto intervalo con media de **0.01s** y distribución exponencial.
* Además tiene un **buffer** de datos que almacena un total de 200 mil paquetes, ya que genera paquetes a una velocidad muy alta tiene que tener un lugar donde guardar estos paquetes.

-imagen-

* El network tiene un queue que conecta `nodeTx` con `nodeRx`, este simula una subred y tiene una capacidad de 200 paquetes como máximo

-imagen-

* El `nodeRx` tiene un buffer de almacenamiento de 200 paquetes, el cual se conecta con un "sink" el cual simula el lugar a donde tienen que llegar los paquetes finalmente.

-imagen-

* Las conexiones entre los distintos nodos cuentan con un delay de propagación de los paquetes entre notos, y un datarate máximo soportado por esa conexión. Estos parámetros los podemos cambiar a nuestro criterio, los que vamos a usar serán los dados por el caso 1 y 2 del enunciado del laboratorio.

## Caso 1 de estudio:

| Parametros    | nodeTx -> Queue |Queue -> nodeRx|nodeRx -> Queue (nodeRx)|Queue (nodeRx) -> Sink|
| ------------- | :-------------: |:-------------:|:----------------------:|:--------------------:|
| delay         |     100 us      |     100 us    | -                      | -                    |
| Datarate      |     1 Mbps      |     1 Mbps    | -                      | 0.5 Mbps             |

### Hipótesis:

En este caso podemos ver que el delay y el datarate para la "ruta" desde nodeTx a nodeRx son todos iguales.

Sin embargo como la conexión que une el Queue interno de nodeRx con el Sink tiene un datarate igual a la mitad del datarate
que tenian las otras conexiones, podemos intuir que se puede dar un cuello de botella en ese buffer, incluso podríamos ir
más allá y decir que cada dos paquetes generados se va a entregar uno, por ende llegará un punto en el cual el buffer del 
nodeRx llegue a su capacidad máxima de 200 paquetes y empiece a generar pérdida de paquetes, ya que no podrá almacenar más
(esto se conoce como problema de **control de flujo**).

Sabiendo que cada 2 paquetes entrega 1, podemos incluso intuir que para cuando hayan salido 400 paquetes de nodeTx va a ser
cuando se dará el problema descrito.

### Mediciones:

Realizamos distinatas mediciones de este caso con distintos interavalos de generación de paquetes, analizando así puntos
críticos como en los que ya no se pierden paquetes (lo cual se daría cuando el intervalo de generación de paquetes es muy grande).

-acá iría un gráfico de las mediciones, tablas y analisis de las mismas-

## Caso 2 de estudio:

| Parametros    | nodeTx -> Queue |Queue -> nodeRx|nodeRx -> Queue (nodeRx)|Queue (nodeRx) -> Sink|
| ------------- | :-------------: |:-------------:|:----------------------:|:--------------------:|
| delay         |     100 us      |     100 us    | -                      | -                    |
| Datarate      |     1 Mbps      |     0.5 Mbps  | -                      | 1 Mbps               |

### Hipótesis:

En este caso podemos ver que la conexión que une el nodeTx con el Queue del network (el que simula una subred) tiene un dataRate de 1Mbps
pero la conexión que une el Queue del network con el nodeRx tiene un datarate de 0.5Mbps lo cual nos indica que se dará
un cuello de botella en ese punto, en el Queue del netwokr.

Similar al caso anterior, cada dos paquetes se entregará uno solo, lo cual a la larga hará que el buffer del Queue se llene
y por ende empiece a haber pérdida de paquetes.

Dado que la cantidad de paquetes que se pueden enviar está limitado por la red, más específicamente la subred, y es esta
la razón de la pérdida de datos, estamos frente a un problema de **control de congestión**

### Mediciones:
Similar al caso anterior.

-acá iría un gráfico de las mediciones, tablas y analisis de las mismas-

## Conclusión:
La conclusión lo haremos en base a los gráficos y las tablas xd

# Red desarrollada:
Esta red sería nuestra propuesta para solucionar el problema de control de flujo y control de congestión que vimos en el
apartado anterior.

Está conformada por un **nodo transmisor** `nodeTx`, un **nodo receptor** `nodeRx` y 2 nods intermedios que
conectan `nodeTx` con `nodeRx`, uno lo usaremos como subred y otro como un canal de comunicación entre estos nodos para que
puedan transmitir datos extra acerca del estado en el que se encuentran.

-imagen-

### Esta red esta desarrollada de la siguiente manera:

-hace tu magia salchi-

## Caso 1 de estudio:

| Parametros    | nodeTx -> Queue |Queue -> nodeRx|nodeRx -> Queue (nodeRx)|Queue (nodeRx) -> Sink|
| ------------- | :-------------: |:-------------:|:----------------------:|:--------------------:|
| delay         |     100 us      |     100 us    | -                      | -                    |
| Datarate      |     1 Mbps      |     1 Mbps    | -                      | 0.5 Mbps             |

### Hipótesis:

-magia salchi-

### Mediciones:

-acá iría un gráfico de las mediciones, tablas y analisis de las mismas-

## Caso 2 de estudio:

| Parametros    | nodeTx -> Queue |Queue -> nodeRx|nodeRx -> Queue (nodeRx)|Queue (nodeRx) -> Sink|
| ------------- | :-------------: |:-------------:|:----------------------:|:--------------------:|
| delay         |     100 us      |     100 us    | -                      | -                    |
| Datarate      |     1 Mbps      |     0.5 Mbps  | -                      | 1 Mbps               |

### Hipótesis:

-magia salchi-

### Mediciones:

-acá iría un gráfico de las mediciones, tablas y analisis de las mismas-

## Conclusión:
La conclusión lo haremos en base a los gráficos y las tablas xd

# Referencias:

- [1] Tanenbaum A. S. (2012). Redes de computadores (5ta ed.) Pearson.
- [2] Kurose, J. F. and Ross, K. W. Computer Networking - A Top Down Approach. 7th Edition, Pearson, 2017
- [3] OMNeT++ Simulation Manual: [Manual de omnet](https://doc.omnetpp.org/omnetpp/manual/)
- [4] ChatGPT (consultas simples de código)
