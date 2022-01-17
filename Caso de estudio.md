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

Este es un método no determinista y se utiliza para que a través de valores probabilísticos se simule el comportamiento impredecible de la realidad con la generación de números semialeatorios.

Si bien es cierto que un mayor número de simulaciones deberían ser más parecidos a los cálculos obtenidos por métodos deterministas, es precisamente con este comportamiento con el que se pueden obtener datos extra como la variabilidad y obtener rangos de comportamiento.

Para este ejercicio específico, se utilizarán tres simulaciones en paralelo en doscientas pruebas diferentes. El primero indicará cuantas piezas se recibirán, como se mencionó anteriormente se utilizará una función beta, este primer número indicará cuantas veces se ejecutará la segunda simulación. La segunda simulación determinará qué dispositivo se ha recibido considerando un número semialeatorio continuo entre 0 y 1, y respecto a la función acumulada de los diferentes modelos indicará a qué modelo y gradación corresponde.

La tercera simulación determina a quién se venderá el equipo, la opción que mejor pague por el dispositivo tendrá una probabilidad del 60%, la segunda mejor opción tendrá una probabilidad del 30% y la tercera opción un 10%.

Se hará una operación aritmética del precio de venta de cada equipo menos el precio de adquisición y se registrará el total en una tabla.

Finalmente se tomarán todos los resultados de la tabla y podremos determinar los números estadísticos descriptivos y conocer el alcance del programa bajo dichas cantidades.

Para poder replicar el análisis en cualquier computadora con el mismo software, se utilizarán semillas en los métodos y funciones que requieran números aleatorios.

---


Due to the behavior of received Devices from the trade in program, it is believed that we will receive five hundred devices per month, however, in order for the simulation to consider scenarios where sales are slightly lower than planned, it is proposed two hundred simulations where a random number of pieces of the beta function $X \sim Beta(\alpha= 4, \beta = 5)$ with location 400 and scale of 200 (**image 1**). This distribution has the characteristic of having a mean ($\overline{X}$) of 488.03, a median ($\widetilde{X}$) of 488.89 and a standard variation ($\sigma$) of 31.43.



<figure><figcaption><b>Image 1.<b> Beta Function for received devices.</figcaption><img src="Image 1.png" alt="Image 1" style="zoom:67%;" /></figure>

Analytics has determined that the equipment reception will have a distribution as indicated in **table 1**. For simulation issues, each received equipment will generate a semi-random number between 0 and 1 to simulate the grade of the device received, only in the event that a unit does not have a price available for grade 3, the price of grade 2 will be taken.

**Table 1. Probability of receiving different grade devices.**

| Grading | Probability of being received |
| ------- | ----------------------------- |
| Grade 1 | 80.00%                        |
| Grade 2 | 15.24%                        |
| Grade 3 | 4.76%                         |

Due to the above, a file containing the probabilities of each device of being acquired by the trade-in program has been restructured, separated into three main columns: Model, grading and probability. The probability has been calculated as follows.
$$
p_{model - grade}=p_{model}\cdot p_{grading}
$$
An example of the above is the **Galaxy Note 10** model, which in the model mix has a probability of receiving it of 0.6%, this amount would be multiplied by each of the probabilities of each grade of being received (**table 1**).
$$
p_{Note10-Grade1}=0.6\% \cdot 80.00\% = 0.4800\%\\
p_{Note10-Grade2}=0.6\% \cdot 15.24\% = 0.0914\%\\
p_{Note10-Grade3}=0.6\% \cdot 4.76\% = 0.0286\%
$$
With the above we can affirm the following, where:

- $p_{i \alpha}$ is the probability of each model of grade 1 to being traded.  

- $p_{i \beta}$ is the probability of each model of grade 2 to being traded.

- $p_{i\gamma}$ Is the probability of each model of grade 3 to being traded. 

- $n$ is the quantity of models on the list.

$$
\sum_{i=1}^{n} ( p_{i \alpha} + p_{i \beta} + p_{i \gamma} ) = 1.00
$$

Since three files have been manipulated, these will be in the annexes, only details of what is contained in each column will be given.

`Probabilities.xlsx` (**table 2**) indicates the probability that a device will be acquired in the trade-in program by model and grading.

**Table 2. Description in Probabilities.xlsx.**

| Column name | Description |
| ----------- | ----------- |
| Device name | Model name. |
| Model Mix | Probability of receiving this model in the trade-in program. |
| Grade | Model grade. |
| Probability | Probability of receiving this model with the corresponding grading in the trade-in program. |

`Buying price.xlsx` (**table 3**) indicates the purchase prices by model and grading.

**Table 3. Description in Buying price.xlsx.**

| Column name | Description |
| ----------- | ----------- |
| Device name | Model name. |
| Grading | Model grade. |
| Buying price | Acquisition price of the model and corresponding grading. |

`Aggregators prices.xlsx` (**table 4**) indicates the prices at which the equipment will be sold, in this specific case it will be considered that 60% of the collected equipment will be sold to the best option, 30% to the second highest bidder and 10 % to the highest bidder.

**Table 4. Aggregators prices.xlsx.**
| Column name | Description |
| ----------- | ----------- |
| Device name | Model name. |
| Grade | Model grade. |
| Selling price 1 | Maximum sale price to aggregators for the model and grading indicated. |
| Selling price 2 | Second highest selling price to aggregators for the model and grading indicated. |
| Selling price 3 | Third highest selling price to aggregators for the designated model and grading. |



## Explanation how Monte Carlo method works

This is a non-deterministic method and it is used so that through probabilistic values the unpredictable behavior of reality is simulated with the generation of semi-random numbers.

Although it is true that a greater number of simulations should be more similar to the calculations obtained by deterministic methods, it is precisely with this behavior that extra data such as variability can be obtained and behavior ranges obtained.

For this specific exercise, three simulations will be used in parallel in two hundred different tests. The first will indicate how many pieces will be received, as previously mentioned a beta function will be used, this first number will indicate how many times the second simulation will be executed. The second simulation will determine which device has been received considering a continuous semi-random number between 0 and 1, and with respect to the accumulated function of the different models it will indicate which model and grading it corresponds to.

The third simulation determines to whom the equipment will be sold, the option that pays the best for the device will have a probability of 60%, the second best option will have a probability of 30% and the third option a 10%.

An arithmetic operation will be made of the sale price of each equipment minus the acquisition price and the total will be recorded in a table.

Finally, all the results of the table will be taken and we will be able to determine the descriptive statistics numbers and know the scope of the program under said quantities.

In order to be able to replicate the analysis on any computer with the same software, seeds will be used in the methods and functions that require random numbers.

## Analysis using Python 3.X

### Step 1



## Annexes

**Annex 1** Creation of **image 1** using python 3.X.

```python
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from matplotlib import ticker

x1 = np.arange(400, 601)
y1 = st.beta(4, 5, loc=400, scale=200).pdf(x1)

fig, ax = plt.subplots(figsize=(6,4))
plt.style.use('bmh')
ax.bar(x, y*100, color='grey', width=3)
ax.set_xlabel('Devices that can be received')
ax.set_ylabel('Probability of receiving those devices')
ax.yaxis.set_major_formatter(ticker.PercentFormatter())
```



![image-20211209231942028](../../../../../Library/Application Support/typora-user-images/image-20211209231942028.png)