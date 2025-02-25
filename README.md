<h1>Laboratory 4 Robotics</h1>

<h2>Team Members</h2>
<ul>
    <li>Juan Carlos Naranjo Jaramillo</li>
    <li>David Santiago Rodríguez Almanza</li>

</ul>
<h3>Universidad Nacional de Colombia 2024-1</h3>
<h3>Table of contents</h3>
<nav id="toc">
    <ul>
        <li><a href="#section1">1. Introduction.</a></li>
        <li><a href="#section2">2. Forward Kinematics.</a></li>
        <li><a href="#section3">3. Python code.</a></li>
        <li><a href="#section4">4. ROS initialization.</a></li>
        <li><a href="#section5">5. Results.</a></li>
        <li><a href="#section6">6. Conclusions.</a></li>
    </ul>
</nav>
<h3 id="section1">1. IIntroduction</h3>
    <p style="text-align: justify;">
    In this report, a step-by-step overview of the development of Robotics Practice 4 is presented. The objective of the practice is to implement the concepts of forward kinematics in a manipulator <b><i>Phantom X Pincher</i></b>.
The specific objectives of the practice include familiarizing oneself with a robotics-oriented development environment such as ROS, utilizing various concepts like topics and services to control the actuators of the manipulator’s joints.

To achieve these objectives, the proposed activity involves developing a Python program that, using <b><i>Dynamixel WorkBench</i></b>, provides the necessary functions to establish communication with the manipulator. This allows us to change the end effector's position from the configuration space, meaning assigning a specific angle to each motor of the robot to orient and position the gripper.

Additionally, a graphical user interface (GUI) is implemented, enabling the selection of one of five possible configurations while displaying the error between the desired and measured angle of each joint.

</p>
    


<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/63e8a2cd-b775-46a7-8e1c-7988cbbbd887" width="400" height="400" />

<h3 id="section2">2. Forward Kinematics.</h3>
<p>The first step is to perform the forward kinematics analysis of the manipulator, which consists of finding the Denavit-Hartenberg (DH) parameter matrix in the HOME position (where the motor sensor values are 0). Then, the loop equation is determined, resulting in a homogeneous transformation matrix (HTM) that represents the end effector relative to the robot's base.

The first step is to measure the distances between the joints of the Phantom X Pincher to obtain the DH parameters. It is important to clarify that the Phantom X Pincher is a robot with four rotational joints and an additional motor in the end effector to control the gripper.</p>

<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/a2154d3a-f234-4981-9c17-ab14199e5fb4" width="400" height="600" />
<h4>DH Parameters</h4>

<table>
    <thead>
        <tr>
            <th>Joint.</th>
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
<p>With this data, we use Peter Corke's toolbox to create the links, and by using the command <code>SerialLink()</code>, we assemble the links to simulate the robot. Then, using the robot-associated function <code>.fkine</code>, we determine the homogeneous transformation matrix (HTM) of the robot's forward kinematics for a given position. For example, for the HOME position, it is:</p>

<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ea194316-e5ff-4911-aff2-cc0a02a41898" width="450" />
<p>Finally, using the <code>teach()</code> method, we plot the robot and can assign desired values to the joints.</p>


<img src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/0fbe5eb4-b61c-404a-8cce-6d60e10bc8c7" width="400" height="500" />
<h3 id="section3">3. Python code.</h3>

<p>The first thing we need to do is initialize the motors in <code>config/basic.yaml</code> using the following structure: </p>
<pre>joint_1_waist:
  ID: 1
  Return_Delay_Time: 0
  # CW_Angle_Limit: 0
  # CCW_Angle_Limit: 2047
  # Moving_Speed: 512</pre>
<p>The same code is repeated for each motor, changing the name and ID.</p>
<p> Now, in the Python file <code>scripts/GUI_Lab4.py</code>, the main functions are described below: </p>

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

<p>This is the general function that calls the services of the <code>dynamixel_workbench package</code> library. It is general because it can receive different commands as an argument. It also takes the motor ID, the desired value for the motor (when a movement is required), and the time in which we want the action to be executed. This time was set to 1 second to allow the robot to move one joint at a time and stabilize before proceeding to the next one.</p>

```python
def move_joint(id, position):
    jointCommand('', id, 'Goal_Position', position, time_execution)
```
<p>This function aims to simplify the way we communicate with the robot, as we frequently use the command <code>Goal_Position</code> to move the joint to a specific degree, and the execution time remains constant. The function only receives the motor ID to be moved and the position where it is desired to be placed.</p>

```python
def listener():
    rospy.init_node('joint_listener', anonymous = True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
```
<p>With this function, it subscribes to a topic from the Dynamixel library, where the positions read by the sensors in the motors are received. Each time data arrives from this topic, the callback function is called.</p>

```python
def callback(data):
    positions_degrees = np.multiply(data.position, 180/pi)
    read_objects = [read1,read2,read3,read4,read5,read6,read7,read8,read9,read10]
    for i in range(5):
        read_objects[i].config(text = str("{:.2f}".format(positions_degrees[i])) + 'º')
        difference = str("{:.2f}".format(next_position_deg[i] - positions_degrees[i]))
        read_objects[i + 5].config(text = difference + 'º')
```
<p>It is used to display the received data on the graphical interface. It iterates through all the values of the data from the sensors, subtracts them from the reference values sent to each motor, and assigns the results to the text attributes of the objects in the <code>read_objects</code> list. </p>

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
<p>The Dynamixel motors receive a number in a 10-bit format, providing a resolution of 1024. The reason it is divided by 300 is due to the angular limit the motor can reach, and 512 is added because this is the value where the motor's zero position is set. </p>

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
<p>After pressing a <code>submit</code> button, this function starts the sequence to move the robot to the position set in a dropdown menu where the 5 required configurations are listed. It then searches in a predefined list for the sequence corresponding to the selected index from the dropdown menu and calls the <code>move_joint</code> function for each motor.</p>
<p>In the following image, you can see how the graphical interface looks when the program starts.</p>
        
![0](https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ee37ecaf-d494-475b-b021-2aa06b4a6881)


<p>When the program starts, the motors are initialized by setting a torque limit for each motor. Then, they are moved to the HOME position, and the listener function is called to begin receiving data from the sensors. Finally, it enters the pop-up window loop, where one of the 5 possible positions can be selected, sent, and the error visualized.</p>

<h3 id="section4">4. ROS Initialization.</h3>
To configure and run the project, the following steps must be performed, WITH THE REAL ROBOT CONNECTED TO THE COMPUTER:
<ol>
    <li>Navigate in the terminal to the base of the project (in this case, being in .../Catkin)</li>
    <li>Run the following command to compile the project:</li>
    <pre> catkin_make source devel/setup.bash</pre>
    <li>Run the following command to see where the real robot is connected:</li>
    <pre>ls /dev/tty*</pre>
    <p>A value of the type /dev/ttyUSB should appear. In this case, it's ttyUSB0. If it's another number, the project code needs to be edited to have the correct number (you can use the replaceAll function in VSCode). If no ttyUSB appears, the robot is not being detected. In this case, disconnect and reconnect. Another useful command is lsusb.</p>
    <li>Run the following command to grant permissions to use the USB port (don’t forget to put the correct port number):</li>
    <pre>sudo chmod 777 /dev/ttyUSB0</pre>
    <li>Run the following command to launch the project:</li>
    <pre>roslaunch phantom_move_position phantom.launch</pre>
</ol>
<h3 id="section5">5. Results</h3>
<p>Next, the robot is shown in the 5 different positions compared to the simulation in MATLAB, as well as the error values displayed on the graphical interface.</p>
<h5>Position 1 [25 25 20 -20 0]</h5>


<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/27625a88-91c9-4410-b8ff-97028cbc7b20">

<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/d1dee128-7ccc-4c4d-82db-15dca98d5933">

<h5>Position 2 [-35 35 -30 30 0]</h5>

<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/2fc7df3e-9a9c-429e-a6d1-a451df0548df">

<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/a07ebf1f-fd9d-42d8-a82f-f42318b0689f">


<h5>Position 3 [85 -20 55 25 0]</h5>
<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/efcfb369-2c02-4921-8dad-2d20433b8456">
<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/aab1b107-9f13-4130-ad66-fd2abd6fc88d">

<h5>Position 4 [80 -35 55 -45 0]</h5>
<img width="450" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/44b8b884-e4fc-4deb-8210-940a56c82141">
<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/3f9e5325-f64d-47da-a5cf-116310c57359">

<h5>Position HOME [0 0 0 0 0]</h5>
<img width="450" alt=image src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/bd674623-bbdd-49bb-8640-fb6fdbfeae9e">
<img width="550" alt="image" src="https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/ee37ecaf-d494-475b-b021-2aa06b4a6881">
<p>Video of operation: For better quality, refer to the "photos" folder.</p>






https://github.com/JuanNaranjo17/Lab4_Robotics/assets/95663629/dd68a237-4e7e-451c-b03c-44d6b59330c2





<h3 id="section6">6. Conclusions</h3>
<p>The DH parameters provide us with a fast, simple, and repeatable method to characterize any type of manipulator. Additionally, Peter Corke's toolbox provides the necessary tools to simulate robots and visualize different configurations quickly and clearly.</p>
<p>On the other hand, we managed to understand the Dynamixel libraries by using topics and services in ROS to establish communication with the robot's actuators. ROS is a very useful software, as simultaneously controlling more than two actuators requires high processing and memory capabilities, which cannot be satisfied using common microcontrollers. Therefore, ROS allows us to easily leverage the capabilities of a much faster processor and more threads to control the hardware.</p>
<p>Finally, from the images, it can be observed that the error of the motors is generally less than one degree. This is an impressive precision for a manipulator primarily used for learning. This performance can be leveraged to perform more complex tasks, opening the door to more interesting projects. </p>











