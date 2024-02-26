# Proyecto Simulacion de Eventos Discretos

##Introduccion
El objetivo de este proyecto es desarrollar una simulacion de eventos discretos para analizar y entender mejor el funcionamiento de la atencion a clientes en sistemas de n servidores en paralelo. A traves de esta simulacion buscamos determinar el tiempo promediode espera de los clientes, el tiempo de ocio de los servidores, maximo de clientes en colla y otros indicadores de rendimiento del sistema.

###Objetivos y metas
Los objetivos principales del proyecto son:

- Desarrollar un modelo de simulacion que represente con presicion el sistema de atencion a clientes en paralelo
- Utilizar el modelo de simulacion para analizar el comportamiento del sistema bajo diferentes condiciones, como el nunmero de servidores, la tasa de llegada de clientes y la distribucion de los tiempos de servicio.
- Obtener resultados que nos ayuden a tomar decisiones informadas sobre como mejorar el rendimiento del sistema.

###Variables que describen el problema
- Numero de servidores: n
- Distrubucion de llegada de cliente: exponencial,uniforme o Poission.
- Distribucion de tiempos de servicio: exponencial, uniforme, poisson o normal.

###Variables de interes:
- Tiempo promedio de espera de los clientes
- Tiempo de ocio de los servidores
- Numero maximo de clientes en cola
- Numero de clientes atendidos
- Porcentaje de clientes que abandonan la cola sin ser atendidos (Si definimos un tamano maximo de la cola o un tiempo de espesa maximo para los clientes)

##Detalles de Implementacion
El proyecto fue implementado en python utilizando numpy para generar las variables aleatorias que sigan ciertas distribuciones y heapq para mantener el orden de la cola de los clientes.
###Pasos principales seguidos para la implementacion:
1. Definimos los modelos para la simulacion:
	- Creamos una clase `Customer` que representa a los clinetes que llegan al sistema
	- Creamos una clase `Server` que representa a los servidores que atienden a los clientes.
2. Implementamos la simulacion:
	- Implementamos la logica de la simulacion en el metodo simulate_system
	- Este metodo se encarga de generar clientes, servidores y actualizar el estado del sistema a lo largo del tiempo
	- Como eventos a simular tenemos la llegada de un cliente al sistema y cuando un servidor termina de atender a un cliente.
3. Analisis de resultados:
	- Calculamos el tiempo promedio de espera de los clientes, el tiempo de ocio de los servidores, maximo de clientes en cola y otros indicadores de rendimiento del sistema.

##Resultados y Experimentos
Realizamos una serie de experimentos  con diferentes configuraciones del sistema de simulacion y los siguientes son algunos de los resultados interpretados:
- El tiempo promedio de espera de los clientes disminuye a medida que aumenta el numero de servidores
- El tiempo de ocio de los servidores disminuye a medida que aumenta la tasa de llegada de clientes
- El numero de maximos clientes en cola aumenta a medida que aumenta la tasa de llegada de clientes y disminuye el numero de servidores
- El porcentaje de clientes que abandona aumenta a medida que aumenta el tiempo promedio de espera

###Interpretacion de los resultados
- Aumentar en numero de servidores es la forma mas efetiva  de reducir el tiempo promedio de espera de los clientes
- Aumentar la tasa de llegadas de cliente es inversamente proporcional a aumentar el numero de servidores
- Dsiminuir el numero de servidores y aumentar la tasa de clientes aumenta el porcetaje de clientes que abandonan la cola sin ser atendidos

###Necesidad de realizar el analisis estadistico de la simulacion
//TODO

###Analisis de parada de la simulacion
Utilizamos dos criterios de parada para la simulacion:
- Numero de clientes atendidos: detenemos la simulacion despues de haber atendido determinado numero de clientes.
- Tiempo de la simulacion: detenemos la simulacion despues de que haya transcurrido un cierto tiempo

##Modelo Matematico
###Descripcion del modelo de simulacion
El modelo de simulación se basa en un modelo matemático que representa el sistema de atención a clientes. El modelo matemático se basa en las siguientes suposiciones:

- Los clientes llegan al sistema de acuerdo con una distribución exponencial.
- Los tiempos de servicio de los clientes se distribuyen de acuerdo con una distribución exponencial.
- Los servidores son independientes entre sí.
- El sistema es de cola simple.

### Supuestos y restricciones

El modelo de simulación se basa en los siguientes supuestos:

- Los clientes llegan al sistema de forma independiente y aleatoria.
- Los tiempos de servicio de los clientes son independientes y aleatorios.
- El sistema es de cola simple, lo que significa que los clientes son atendidos por uno y solo un servidor.

El modelo de simulación tiene las siguientes restricciones:

- El número de servidores es fijo.
- La tasa de llegada de clientes es fija.
- La distribución de los tiempos de servicio de los clientes es fija.

El modelo de simulación se puede utilizar para analizar el comportamiento del sistema bajo diferentes condiciones, como el número de servidores, la tasa de llegada de clientes y la distribución de los tiempos de servicio.

###Modelo Matematico
El modelo matemático de un sistema de servidores en paralelo se basa en la teoría de colas. Las siguientes son algunas de las fórmulas y relaciones más importantes del modelo:

* **Tiempo promedio de espera de los clientes:**
    ```
    W = \\frac{\\lambda}{C(1-\\rho)}
    ```
    donde:
    * W es el tiempo promedio de espera de los clientes
    * \\lambda es la tasa de llegada de los clientes
    * C es el número de servidores
    * \\rho es la tasa de utilización del sistema
* **Tiempo promedio de servicio de los clientes:**
    ```
    S = 1 / \\mu
    ```
    donde:
    * S es el tiempo promedio de servicio de los clientes
    * \\mu es la tasa de servicio de los clientes
* **Tasa de utilización del sistema:**
    ```
    \\rho = \\lambda / (\\mu C)
    ```
    donde:
    * \\rho es la tasa de utilización del sistema
    * \\lambda es la tasa de llegada de los clientes
    * \\mu es la tasa de servicio de los clientes
    * C es el número de servidores
* **Número promedio de clientes en el sistema:**
    ```
    L = \\lambda W
    ```
    donde:
    * L es el número promedio de clientes en el sistema
    * \\lambda es la tasa de llegada de los clientes
    * W es el tiempo promedio de espera de los clientes
* **Número promedio de clientes en cola:**
    ```
    L_q = \\lambda W_q
    ```
    donde:
    * L_q es el número promedio de clientes en cola
    * \\lambda es la tasa de llegada de los clientes
    * W_q es el tiempo promedio de espera de los clientes en cola'
