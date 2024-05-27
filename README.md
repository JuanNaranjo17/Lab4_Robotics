<h1>Laboratorio 4 Robótica</h1>

<h2>Integrantes</h2>
<ul>
    <li>Juan Carlos Naranjo Jaramillo</li>
    <li>David Santiago Rodríguez Almanza</li>

</ul>
<h3>Universidad Nacional de Colombia 2024-1</h3>
<h3>Tabla de Contenidos</h3>
<nav id="toc">
    <ul>
        <li><a href="#section1">1. Introducción.</a></li>
        <li><a href="#section2">2. Cinematica directa.</a></li>
        <li><a href="#section3">3. Código Matlab.</a></li>
        <li><a href="#section4">4. Código en python.</a></li>
        <li><a href="#section4">5. Resultados.</a></li>
        <li><a href="#section4">6. Conclusiones.</a></li>
    </ul>
</nav>
<h3 id="section1">1. Introducción</h3>
    <p>En el presente informe se presenta el paso a paso del desarrollo de la practica 4 de robotica. El objetivo de la practica es implementar los conceptos
    de cinematica directa en un manipulador <b><i>Phantom X Pincher</i></b> Los objetivos especificos de la practica consisten en familiarizarse con un entorno 
    de desarrollo orientado a la robotica como lo es ROS, haciendo uso de los distintos conceptos como los topicos y servicios, para controlar los actuadores de las 
    articulaciones de un manipulador. Para alcanzar dichos objetivos, la actividad propuesta consiste en desarrollar un programa en python, que haciendo uso del 
    <b><i>Dynamyxel WorkBench</i></b> que nos provee de las funciones necesarias para establecer la comunicacion con el manipulador, podamos desde el espacio de las        configuraciones, cambiar la posicion del efector final. En otras palabras, asignar un angulo especifico a cada motor del robot, para orientar y posicionar las          pinzas en 4 puntos diferentes. Adicionalmente, se realiza una interfaz grafica GUI, que permite seleccionar una de las 5 configuraciones posibles, y muestra el 
    error entre el angulo deseado y el angulo medido de cada articulacion </p>
    
![image](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/63e8a2cd-b775-46a7-8e1c-7988cbbbd887)
    

<h3 id="section1">2. Cinemática directa.</h3>
<p>Lo primero que se procede a hacer, es el analisis de cinematica directa del manipulador, el cual consiste en hallar la matriz de parametros Denavit-Hartenberg (DH) en la posicion de HOME, (donde el valor de los sensores de los motores es 0), para luego encontrar la ecuacion de lazo, la cual resulta en una MTH que me representa el efector final desde la base del robot. El primer paso entonces es tomar las medidas entre las articulaciones del Phantom Pincher para luego obtener los parámetros DH, Cabe aclarar, que el phantom pitcher es un robot de 4 articulaciones rotacionales, con un motor en el efector final para controlar las pinzas del manipulador.</p>

![image](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/a2154d3a-f234-4981-9c17-ab14199e5fb4)

<h4>Parámetros DH</h4>

<table>
    <thead>
        <tr>
            <th>Articulacion.</th>
            <th>a</th>
            <th>&alpha;<sub>i</sub></th>
            <th>d<sub>i</sub></th>
            <th>&theta;<sub>i</sub></th>
            <th>offset</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>0</td>
            <td>&pi;/2</td>
            <td>0</td>
            <td>q<sub>1</sub></td>
            <td>&pi;/2</td>
        </tr>
        <tr>
            <td>2</td>
            <td>10.48</td>
            <td>0</td>
            <td>0</td>
            <td>q<sub>2</sub></td>
            <td>&pi;/2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>10.48</td>
            <td>0</td>
            <td>0</td>
            <td>q<sub>3</sub></td>
            <td>0</td>
        </tr>
        <tr>
            <td>4</td>
            <td>7.576</td>
            <td>0</td>
            <td>0</td>
            <td>q<sub>4</sub></td>
            <td>0</td>
        </tr>
    </tbody>
</table>
<p>Con estos datos, utilizamos el toolbox de Peter Corke para crear eslabones, y utilizando el comando <code>SerialLink()</code>, articulamos los eslabones para simular el robot, luego utilzando la funcion asociada al robot <code>.fkine</code> encontramos la MTH de la cinematica directa del robot para una posicion dada, por ejemplo para la posicion de HOME es :</p>

![image](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ea194316-e5ff-4911-aff2-cc0a02a41898)

<p>Finalmente, haciendo uso del metodo <code>teach()</code>, graficamos el robot, y podemos asignarle valores a las articulaciones que deseemos</p>

![image](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/0fbe5eb4-b61c-404a-8cce-6d60e10bc8c7)

<h3 id="section1">3. Código en python.</h3>
<p></p>

