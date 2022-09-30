# Apliación del método Monte Carlo a un ejemplo que incluye márgenes negativos.

Por Marco A. de la Cruz

## Importante

La información contenida en este ejemplo, así como el planteamiento son ficticios. Este trabajo tiene como finalidad ejemplificar el uso del método Monte Carlo y cómo este puede ser replicado para algùn uso concreto.

Lo contenido en este trabajo es de acceso libre, sin embargo, pido de la ayuda del lector para dar crédito al autor original si este es usado para otros trabajos o estudios.

## Planteamiento del problema

Una empresa dedicada a la venta de joyería ha optado por una estrategia agresiva, para atraer mayor mercado algunos de los precios de ciertos modelos estarán **por debajo de los costos de adquisición**. El equipo de mercadeo estima un aumento de sus clientes y creen que las ventas tendrán un comportamiento de una distribución normal con un promedio de 1000 y una desviación estándar de 100 ($N(\mu = 1000, \sigma = 100)$).

Por otro lado se debe considerar que esta empresa tiene una alianza comercial con una tarjeta de descuentos, el equipo de mercadeo ha indicado que consideran que hay una probabilidad del 20% de un cliente se presente con una tarjeta de descuentos plata, la cual permitiría un descuento del 5% en cualquier producto y que hay una probabilidad del 10% de que un cliente se presente con una tarjeta de descuentos oro, que permitirá adquirir un producto con 10% de descuento.

| Tarjeta de descuentos | % que un cliente use la tarjeta | Descuento en el precio final |
|---|---|---|
| TDD plata | 20% | (-)5% |
| TDD oro | 10% | (-)10% |

Por último se compartió el porcentaje de ventas de cada modelo, y se estima que esa razón se mantendrá en los meses siguientes, por lo que se puede considerar como la probabilidad de que cada modelo sea vendida.

Toda esta información está contenida en el archivo _Prices.xlsx_, la primera columna el artículo, la segunda columna el precio de venta, la tercera columna el costo unitario, y la última la probabilidad de que ese modelo sea vendido.

|Artículo|Precio|Costo|Probabilidad|
|---|---|---|---|
|Item #1|\$ 4 600.00|\$ 4 830.00|2.79%|
|Item #2|\$ 4 100.00|\$ 4 080.00|4.70%|
|Item #3|\$ 2 500.00|\$ 1 575.00|8.26%|
|Item #4|\$ 4 400.00|\$ 4 004.00|5.78%|
|Item #5|\$ 5 000.00|\$ 3 600.00|9.71%|
|Item #6|\$ 5 000.00|\$ 5 350.00|6.60%|
|Item #7|\$ 2 700.00|\$ 1 998.00|7.13%|
|Item #8|\$ 2 200.00|\$ 2 068.00|0.39%|
|Item #9|\$ 2 600.00|\$ 2 288.00|5.94%|
|Item #10|\$ 2 800.00|\$ 3 080.00|2.48%|
|Item #11|\$ 2 500.00|\$ 2 800.00|2.32%|
|Item #12|\$ 2 300.00|\$ 2 553.00|6.98%|
|Item #13|\$ 4 000.00|\$ 3 800.00|8.48%|
|Item #14|\$ 4 800.00|\$ 2 928.00|0.69%|
|Item #15|\$ 3 900.00|\$ 3 550.00|1.98%|
|Item #16|\$ 2 700.00|\$ 2 322.00|3.18%|
|Item #17|\$ 4 400.00|\$ 3 784.00|6.36%|
|Item #18|\$ 3 300.00|\$ 3 105.00|8.46%|
|Item #19|\$ 4 700.00|\$ 3 478.00|3.69%|
|Item #20|\$ 4 800.00|\$ 3 840.00|4.08%|

Para este ejemplo no se considerán otros costos (por ejemplo, costos fijos) más allá que los costos unitarios, además no se considerarán los impuestos. Esto con la finalidad de simplificar este ejercicio y dar a entender el funcionamiento del método Monte Carlo.

Para dar un poco más de profesionalidad al trabajo he optado por mostrar toda esta información en un archivo _Latex_, ya que como ejemplo esto puede ser empleado en un fomrsto estándar (como el que se usa para tesis y trabajos similares).

## Explicación de cómo funciona el método Monte Carlo

Este es un método no determinista y se utiliza para que, a través de valores probabilísticos, se simule el comportamiento impredecible de la realidad con la generación de números semialeatorios.

Si bien es cierto que un mayor número de simulaciones deberían ser más parecidos a los cálculos obtenidos por métodos deterministas, es precisamente con este comportamiento con el que se pueden obtener datos extra como la variabilidad y obtener rangos de comportamiento.

Para este ejercicio específico, se utilizarán tres simulaciones en paralelo en doscientas pruebas diferentes. El primero indicará cuásntas piezas se recibirán, como se mencionó anteriormente se utilizará una función beta, este primer número indicará cuantas veces se ejecutará la segunda simulación. La segunda simulación determinará qué dispositivo se ha recibido considerando un número semialeatorio continuo entre 0 y 1, y respecto a la función acumulada de los diferentes modelos indicará a qué modelo y gradación corresponde.

La tercera simulación determina a quién se venderá el equipo, la opción que mejor pague por el dispositivo tendrá una probabilidad del 60%, la segunda mejor opción tendrá una probabilidad del 30% y la tercera opción un 10%.

Se hará una operación aritmética del precio de venta de cada equipo menos el precio de adquisición y se registrará el total en una tabla.

Finalmente se tomarán todos los resultados de la tabla y podremos determinar los números estadísticos descriptivos y conocer el alcance del programa bajo dichas cantidades.

Para poder replicar el análisis en cualquier computadora con el mismo software, se utilizarán semillas en los métodos y funciones que requieran números aleatorios.

## Resultados

Como se muestra en el archivo Jupyter Notebook se hicieron doscientas simulaciones con los siguientes resultados:

|Monto vendido|Costo|Margen de ganancia|Piezas vendidas|
|---|---|---|---|
|Conteo|200|200|200|
|Promedio|3 627 224|3 271 229|355 995|
|Desviación estándar|348 930|317 552|35 017|
|Valor mínimo|2 776 960|2 506 646|270 314|
|Percentil 25|3 394 261|3 067 201|333 321|
|Percentil 50|3 608 312|3 254 833|357 096|
|Percentil 75|3 864 131|3 471 480|380 254|
|Valor máximo|4 577 485|4 131 135|446 350|

Con una certeza del 95% los promedio poblacionales (no muestrales como la tabla anterior) son de:

- Piezas recibidas, entre 988.95 y 1 016.09.
- Monto vendido, entre 3 689 112.74 y 3 590 058.31

- Costo total, entre 3 236 185.41 y 3 325 409.11
- Ganancia total, entre 353 184.11 y 364 392.42

Si la empresa que vende joyas está dispuesto a ganar el monto promedio como lo indicado arriba, dada la inversión de comprar las piezas y asumir los costos fijos que derriban de ellos podrían optar por la estrategia de vender más barato de lo que compran, sin embargo, si consideran que el margen ganado no amerita el esfuerzo podrían optar por otras alternativas.

