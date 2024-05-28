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
        <li><a href="#section3">3. Código en python.</a></li>
        <li><a href="#section4">4. Inicialización de ROS.</a></li>
        <li><a href="#section5">5. Resultados.</a></li>
        <li><a href="#section6">6. Conclusiones.</a></li>
    </ul>
</nav>
<h3 id="section1">1. Introducción</h3>
    <p style="text-align: justify;">
    En el presente informe se presenta el paso a paso del desarrollo de la practica 4 de robótica. El objetivo de la práctica es implementar los conceptos
    de cinemática directa en un manipulador <b><i>Phantom X Pincher</i></b> Los objetivos específicos de la práctica consisten en familiarizarse con un entorno 
    de desarrollo orientado a la robótica como lo es ROS, haciendo uso de los distintos conceptos como los tópicos y servicios, para controlar los actuadores de las 
    articulaciones de un manipulador. Para alcanzar dichos objetivos, la actividad propuesta consiste en desarrollar un programa en python, que haciendo uso del 
    <b><i>Dynamyxel WorkBench</i></b> que nos provee de las funciones necesarias para establecer la comunicación con el manipulador, podamos desde el espacio de las       configuraciones, cambiar la posición del efector final. En otras palabras, asignar un ángulo específico a cada motor del robot, para orientar y posicionar las         pinzas. Adicionalmente, se realiza una interfaz gráfica GUI, que permite seleccionar una de las 5 configuraciones posibles, y muestra el 
    error entre el ángulo deseado y el ángulo medido de cada articulación </p>
    


<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/63e8a2cd-b775-46a7-8e1c-7988cbbbd887" width="400" height="400" />

<h3 id="section2">2. Cinemática directa.</h3>
<p>Lo primero que se procede a hacer, es el análisis de cinemática directa del manipulador, el cual consiste en hallar la matriz de parámetros Denavit-Hartenberg (DH) en la posición de HOME, (donde el valor de los sensores de los motores es 0), para luego encontrar la ecuación de lazo, la cual resulta en una MTH que me representa el efector final desde la base del robot. El primer paso entonces es tomar las medidas entre las articulaciones del Phantom Pincher para luego obtener los parámetros DH, Cabe aclarar, que el phantom pincher es un robot de 4 articulaciones rotacionales, con un motor en el efector final para controlar las pinzas del manipulador.</p>

<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/a2154d3a-f234-4981-9c17-ab14199e5fb4" width="400" height="600" />
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
<p>Con estos datos, utilizamos el toolbox de Peter Corke para crear eslabones, y utilizando el comando <code>SerialLink()</code>, articulamos los eslabones para simular el robot, luego utilizando la función asociada al robot <code>.fkine</code> encontramos la MTH de la cinemática directa del robot para una posición dada, por ejemplo para la posición de HOME es:</p>

<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ea194316-e5ff-4911-aff2-cc0a02a41898" width="450" />
<p>Finalmente, haciendo uso del método <code>teach()</code>, graficamos el robot, y podemos asignarle valores a las articulaciones que deseemos</p>


<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/0fbe5eb4-b61c-404a-8cce-6d60e10bc8c7" width="400" height="500" />
<h3 id="section3">3. Código en python.</h3>

<p>Lo primero que debemos hacer, es inicializar los motores en <code>config/basic.yaml</code> utilizando la siguiente estructura: </p>
<pre>joint_1_waist:
  ID: 1
  Return_Delay_Time: 0
  # CW_Angle_Limit: 0
  # CCW_Angle_Limit: 2047
  # Moving_Speed: 512</pre>
<p>Se repite para cada motor el mismo codigo cambiando nombre e ID.</p>
<p> Ahora bien, en el archivo de python <code>scripts/GUI_Lab4.py</code>, se describen a continuación las funciones principales: </p>

```python
def jointCommand(command, id_num, addr_name, value, time):
    rospy.init_node('joint_node', anonymous=False)
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:   
        print(str(exc))
```

<p>Esta es la función general que llama a los servicios de la librería <code>dynamixel_workbench package</code> es general porque como argumento puede recibir diferentes comandos, también recibe el ID del motor a manejar, el valor en el cual queremos el motor (cuando requerimos de un desplazamiento) y el tiempo en el que queremos que se ejecute la acción. Este tiempo fue definido en 1 segundo, para darle el tiempo al robot de que mueva una sola articulación a la vez, y se alcance a estabilizar antes de seguir a la siguiente.</p>

```python
def move_joint(id, position):
    jointCommand('', id, 'Goal_Position', position, time_execution)</pre>
```
<p>Esta función lo que busca es simplificar la manera de comunicarnos con el robot, dado que utilizamos frecuentemente el comando <code>Goal_Position</code> para mover la articulación a un determinado grado, y el tiempo de ejecución se deja constante, la función recibe únicamente el ID del motor a mover y la posición a donde se desea colocar.</p>

```python
def listener():
    rospy.init_node('joint_listener', anonymous = True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
```
<p>Con esta función, se suscribe a un tópico de la librería dynamixel, donde llegan las posiciones leídas por los sensores en los motores, cada vez que llegue un dato de este tópico se llama a la función callback</p>

```python
def callback(data):
    positions_degrees = np.multiply(data.position, 180/pi)
    read_objects = [read1,read2,read3,read4,read5,read6,read7,read8,read9,read10]
    for i in range(5):
        read_objects[i].config(text = str("{:.2f}".format(positions_degrees[i])) + 'º')
        difference = str("{:.2f}".format(next_position_deg[i] - positions_degrees[i]))
        read_objects[i + 5].config(text = difference + 'º')
```
<p>Sirve para poder mostrar los datos recibidos en la interfaz gráfica,se recorre todos los valores en de los datos que hay en los sensores, y se restan con los valores de referencia que se le mandan a cada motor, y se le asignan a los atributos de texto de los objetos en la lista  <code>read_objects</code> </p>

```python
def deg_to_motor(degrees):
    data_return = round((1024/300)*degrees + 512)
    if data_return > 1023: 
        print('Check the joint configuration data')
        return 1023
    elif data_return < 0: 
        print('Check the joint configuration data')
        return 0
    else: 
        return data_return
```
<p>Los motores dynamixel reciben un número en formato <code>Unit32</code>, por lo que es necesario transformar el número que deseemos en grados a <code>Unit32</code>, la razón por la que se divide entre 300 es por el límite de ángulo al cual podemos llegar, y se le suman 512, dado que este es el valor donde el motor tiene seteado su cero. </p>

```python
def move_to_point():
    global next_position_deg
    submit_button.config(state = 'disabled')
    close_button.config(state = 'disabled')
    value_pos = int(option_list.index(value_inside.get()))
    next_position_deg = points[value_pos]
    for i in range(5):
        move_joint(joints_IDs[i], deg_to_motor(next_position_deg[i]))
    submit_button.config(state = 'normal')
    close_button.config(state = 'normal')
```
<p>Luego de oprimir un botón de <code>sumbit</code>, esta función inicia la secuencia para poder mover el robot a la posición que ha sido puesta en un menú desplegable donde están las 5 configuraciones que nos piden, entonces busca en una lista establecida al inicio del código la secuencia correspondiente con el índice que esté seleccionado del menú desplegable, y llama a la función <code>move_joint</code> por cada motor.</p>
<p>En la siguiente imagen se puede apreciar como se ve la interfaz grafica al iniciar el programa</p>
        
![0](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ee37ecaf-d494-475b-b021-2aa06b4a6881)


<p>Al iniciar el programa se inicializan los motores, al definir un torque límite de cada motor, posteriormente se lleva a la posición de HOME, y se llama a la función listener para empezar a recibir datos de los sensores, finalmente se entra en el loop de la ventana emergente, donde se puede seleccionar una de las 5 posiciones posibles, enviarlas y visualizar el error.</p>

<h3 id="section4">4. Inicializacion en ROS.</h3>
Para configurar y ejecutar el proyecto se debe realizar lo siguiente, CON EL ROBOT REAL CONECTADO AL COMPUTADOR:
<ol>
    <li>Navegar en la terminal hasta la base del proyecto (en este caso, estar en .../Catkin)</li>
    <li>Correr el siguiente comando para compilar el proyecto:</li>
    <pre> catkin_make source devel/setup.bash</pre>
    <li>Correr el siguiente comando para ver dónde está conectado el robot real:</li>
    <pre>ls /dev/tty*</pre>
    <p>Debería aparecer un valor del tipo /dev/ttyUSB. En este caso, es ttyUSB0, en caso de ser otro número, se debe 
    editar el código del proyecto para tener el número correcto (se puede usar la función replaceAll de VSCode).
    En caso de que no aparezca ningún ttyUSB el robot no está siendo detectado. En este caso, desconectar y conectar 
    nuevamente. Otro comando de interés es lsusb.</p>
    <li>Correr el siguiente comando para otorgar los permisos para el uso del puerto USB (no olvidar poner el número 
    del puerto correcto):</li>
    <pre>sudo chmod 777 /dev/ttyUSB0</pre>
    <li>Correr el siguiente comando para lanzar el proyecto:</li>
    <pre>roslaunch phantom_move_position phantom.launch</pre>
</ol>
<h3 id="section5">5. Resultados</h3>
<p>A continuación, se muestra el robót en las 5 posiciones diferentes comparadas con la simulación en MATLAB, así como los valores de error mostrados en la interfaz gráfica</p>
<h5>Posición 1 [25 25 20 -20 0]</h5>


<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/27625a88-91c9-4410-b8ff-97028cbc7b20">

<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/d1dee128-7ccc-4c4d-82db-15dca98d5933">

<h5>Posición 2 [-35 35 -30 30 0]</h5>

<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/2fc7df3e-9a9c-429e-a6d1-a451df0548df">

<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/a07ebf1f-fd9d-42d8-a82f-f42318b0689f">


<h5>Posición 3 [85 -20 55 25 0]</h5>
<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/efcfb369-2c02-4921-8dad-2d20433b8456">
<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/aab1b107-9f13-4130-ad66-fd2abd6fc88d">

<h5>Posición 4 [80 -35 55 -45 0]</h5>
<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/44b8b884-e4fc-4deb-8210-940a56c82141">
<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/3f9e5325-f64d-47da-a5cf-116310c57359">

<h5>Posición HOME [0 0 0 0 0]</h5>
<img width="450" alt=image src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/bd674623-bbdd-49bb-8640-fb6fdbfeae9e">
<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ee37ecaf-d494-475b-b021-2aa06b4a6881">
<p>Video funcionamiento</p>


https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/5352ebf1-a64b-4c2e-a120-8b8aef35b1fe

<h3 id="section6">6. Conclusiones</h3>
<p>Los parámetros de DH, nos otorga un método rápido, sencillo y repetible para poder caracterizar cualquier tipo de manipulador, adicionalmente, el toolbox de peter corke nos otorga las herramientas necesarias para poder simular los robots, y visualizar diferentes configuraciones de manera rápida y clara.</p>
<p>Por otra parte, se logró entender las librerías de dynamixel, haciendo uso de los tópicos y servicios re ROS para poder establecer una comunicación con los actuadores del robot. ROS es un software muy útil, dado que controlar simultáneamente más de 2 actuadores requiere una capacidad de procesamiento y memoria elevadas, las cuales no pueden ser satisfechas usando microcontroladores comunes, por lo que ROS nos permite usar de manera sencilla las capacidades de un procesador mucho más rápido y más hilos para hacer control de hardware.</p>
<p>Finalmente, de las imágenes se observa que el error de los motores es por lo general de menos de un grado. Una precisión impresionante para un manipulador utilizado principalmente para el aprendizaje, este desempeño puede ser aprovechado para realizar tareas de mayor complejidad, abriendo la puerta a proyectos más interesantes </p>











