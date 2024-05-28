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
    <p>En el presente informe se presenta el paso a paso del desarrollo de la practica 4 de robotica. El objetivo de la practica es implementar los conceptos
    de cinematica directa en un manipulador <b><i>Phantom X Pincher</i></b> Los objetivos especificos de la practica consisten en familiarizarse con un entorno 
    de desarrollo orientado a la robotica como lo es ROS, haciendo uso de los distintos conceptos como los topicos y servicios, para controlar los actuadores de las 
    articulaciones de un manipulador. Para alcanzar dichos objetivos, la actividad propuesta consiste en desarrollar un programa en python, que haciendo uso del 
    <b><i>Dynamyxel WorkBench</i></b> que nos provee de las funciones necesarias para establecer la comunicacion con el manipulador, podamos desde el espacio de las configuraciones, cambiar la posicion del efector final. En otras palabras, asignar un angulo especifico a cada motor del robot, para orientar y posicionar las pinzas. Adicionalmente, se realiza una interfaz grafica GUI, que permite seleccionar una de las 5 configuraciones posibles, y muestra el 
error entre el angulo deseado y el angulo medido de cada articulacion </p>
    


<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/63e8a2cd-b775-46a7-8e1c-7988cbbbd887" width="400" height="400" />

<h3 id="section2">2. Cinemática directa.</h3>
<p>Lo primero que se procede a hacer, es el analisis de cinematica directa del manipulador, el cual consiste en hallar la matriz de parametros Denavit-Hartenberg (DH) en la posicion de HOME, (donde el valor de los sensores de los motores es 0), para luego encontrar la ecuacion de lazo, la cual resulta en una MTH que me representa el efector final desde la base del robot. El primer paso entonces es tomar las medidas entre las articulaciones del Phantom Pincher para luego obtener los parámetros DH, Cabe aclarar, que el phantom pitcher es un robot de 4 articulaciones rotacionales, con un motor en el efector final para controlar las pinzas del manipulador.</p>

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
<p>Con estos datos, utilizamos el toolbox de Peter Corke para crear eslabones, y utilizando el comando <code>SerialLink()</code>, articulamos los eslabones para simular el robot, luego utilzando la funcion asociada al robot <code>.fkine</code> encontramos la MTH de la cinematica directa del robot para una posicion dada, por ejemplo para la posicion de HOME es :</p>

<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ea194316-e5ff-4911-aff2-cc0a02a41898" width="300" height="150" />
<p>Finalmente, haciendo uso del metodo <code>teach()</code>, graficamos el robot, y podemos asignarle valores a las articulaciones que deseemos</p>


<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/0fbe5eb4-b61c-404a-8cce-6d60e10bc8c7" width="400" height="500" />
<h3 id="section3">3. Código en python.</h3>

<p>Lo primero que debemos hacer, es inicializar los motores en <code>config/basic.yaml</code> utilizando la siguiente estructura: 
<pre>joint_1_waist:
  ID: 1
  Return_Delay_Time: 0
  # CW_Angle_Limit: 0
  # CCW_Angle_Limit: 2047
  # Moving_Speed: 512</pre>
Se repite para cada motor el mismo codigo cambiando nombre e ID.</p>
<p> Ahora bien, en el archivo de python <code>scripts/GUI_Lab4.py</code>, se describen a continuacion las funciones principales: </p>

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

<p>Esta es la función general que llama a los servicios de la libreria <code>dynamixel_workbench package</code> es general porque como argumento puede recibir diferentes comandos, tambien recibe el ID del motor a manejar, el valor en el cual queremos el motor (cuando requerimos de un desplazamiento) y el tiempo en el que queremos que se ejecute la acción. este tiempo fue definido en 1 segundo, para darle el tiempo al robot de que mueva una sola articulacion a la vez, y se alcance a estabilizar antes de seguir a la siguiente.</p>

```python
def move_joint(id, position):
    jointCommand('', id, 'Goal_Position', position, time_execution)</pre>
```
<p>Esta fucncion lo que busca es simplificar la manera de comunicarnos con el robot, dado que utilizamos frecuentemente el comando <code>Goal_Position</code> para mover la articulacion a un determinado grado, y el tiempo de ejecucion se deja constante, la funcion recibe unicamente el id del motor a mover y la posicion a donde se desea colocar.</p>

```python
def listener():
    rospy.init_node('joint_listener', anonymous = True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
```
<p>Con esta funcion, se suscribe a un topico de la libreria dynamixer, donde llegan las posiciones leidas por los sensores en los motores, cada vez que llegue un dato de este topico se llama a la funcion callback</p>

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
<p>Los motores dynamixel reciben un numero en formato <code>Unit32</code>, por lo que es necesario transformar el numero que deseemos en grados a <code>Unit32</code>, la razon por la que se divide entre 300 es por el limite de anggulo al cual podemos llegar, y se le suman 512, dado que este es el valor donde el motor tiene seteado su cero. </p>

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
<p>Luego de oprimir un botón de <code>sumbit</code>, esta funcion inicia la secuencia para poder mover el robot a la posicion que ha sido puesta en un menú desplegable donde estan las 5 configuraciones que nos piden, entonces busca en una lista establecida al inicio del codigo la secuencia correspondiente con el indice que este seleccionado del menu desplegable, y llama a la funcion <code>move_joint</code> por cada motor.</p>
<p>En la siguiente imagen se puede apreciar como se ve la interfaz grafica al iniciar el programa</p>
        
![0](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ee37ecaf-d494-475b-b021-2aa06b4a6881)


<p>Al iniciar el programa se inicializan los motores, al definir un torque limite de cada motor, posteriormente se lleva a la posicion de HOME, y se llama a la funcion listener para empezar a recibir datos de los sensores, finalmente se entra en el loop de la ventana emergente, donde se puede seleccionar una de las 5 posiciones posibles, enviarlas y visualizar el error.</p>

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
