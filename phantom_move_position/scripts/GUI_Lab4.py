#!/usr/bin/env python

import tkinter as tk
from dynamixel_workbench_msgs.srv import DynamixelCommand
from sensor_msgs.msg import JointState
import rospy
import numpy as np
from cmath import pi


__author__ = "Juan Naranjo"
__credits__ = ["Juan Naranjo"]
__email__ = "jnaranjoj@unal.edu.co"
__status__ = "Test"

# Degrees configuration
points = [
    [0,0,0,0,0],
    [25,25,20,-20,0],
    [-35,35,-30,30,0],
    [85,-20,55,25,0],
    [80,-35,55,-45,0]
]

next_position_deg = points[0]

# Torque definition joint treshhold
torques = [800,600,600,500,500]

# Joint names in configuration file (.yaml)
#joints_IDs = ['waist','shoulder','elbow','wrist','gripper']
joints_IDs = [1,2,3,4,5]

# GUI parameters
font_type = "maiandra_gd"
background_type = "#65A8E1"

# Time execution
time_execution = 1

# General function that calls the services of dynamixel_workbench package, it's general because receive as argument the command name
# Receives also the ID motor, the value for ser a motor variable and the execution time
def jointCommand(command, id_num, addr_name, value, time):
    #rospy.init_node('joint_node', anonymous=False)
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:   
        print(str(exc))

# Function that after press the submit button, starts the sequence for move the robot joints to a specific set configuration in the points list
# The function moves just one servo-motor at a time, starting by the waist and continuing in ascending order till arrive to the wrist
# The motors don't receive a message in degrees, they receive an unsigned int32, and the treshold limits in degrees are -150º and 150º respectively
# so it's neccesary do a convertion between degrees and Uint32 with the function deg_to_motor() before send the request to move_joint function
# We block the buttons for avoid send two robot configurations at the same time because the second configuration could interrupt the first
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

    #read1.config(text = str(value_pos))
    #print(value_pos)

# The move_joint function sends the arguments neccesaries for the function jointCommand to organize the request to a dynamixel_workbench_controller service
# The function sends the motor ID and the service name, also the arguments for do the service message
def move_joint(id, position):
    jointCommand('', id, 'Goal_Position', position, time_execution)

# Function for set the joint mesure values in the graphic interface user
# The data position message is given in radians, so it's necessary do a converstion to degrees
def callback(data):
    positions_degrees = np.multiply(data.position, 180/pi)
    read_objects = [read1,read2,read3,read4,read5,read6,read7,read8,read9,read10]
    for i in range(5):
        read_objects[i].config(text = str("{:.2f}".format(positions_degrees[i])) + 'º')
        difference = str("{:.2f}".format(next_position_deg[i] - positions_degrees[i]))
        read_objects[i + 5].config(text = difference + 'º')

# Node that subscribes to a joint_listener topic for receive the motor joint position messages
# Everytime that the function receives a new message, it calls the callback function.
def listener():
    rospy.init_node('joint_listener', anonymous = True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)

# Function that converts degrees in Uint32, it's important to know that the zero position is equals to 512
# We have 1024 possible numbers and 300º, so the slope is 1024/300
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

# Function for close the GUI and back the robot to home position
def close_window():
    go_home()
    root.destroy()

# Function for send the robot to home position
def go_home():
    home_position_motor = deg_to_motor(0)
    for i in range(5):
        jointCommand('', joints_IDs[i], 'Goal_Position', home_position_motor, time_execution)

###################################################################################################################################################################################################
# GUI configuration and visualitation

# Definition of main window root with the parameters
root = tk.Tk()
root.title("Forward Cinematic Phantom")
root.geometry("640x720")
root.config(background = background_type)
root.resizable(False,False)

# First frame for put the members names and the University logo
frame1 = tk.Frame(root, background = background_type)
frame1.pack(pady = 15)

tk.Label(frame1, text = "Phantom X Pincher Robot Control ", anchor = 'center', justify = "center", foreground = 'white', background = background_type, font = (font_type, 16)).pack()

tk.Label(frame1, text = "Juan Naranjo", background = background_type, font = (font_type, 12)).pack()
tk.Label(frame1, text = "David Rodriguez", background = background_type, font = (font_type, 12)).pack()

image_path = "/home/juan/catkin_ws/src/phantom_move_position/photos/logo_unal.png"
Unal_photo = tk.PhotoImage(file = image_path)
logo = tk.Label(frame1, image = Unal_photo)
logo.config(background=background_type)
logo.pack()

# Second frame for define the selection point interface
frame2 = tk.Frame(root, background = background_type)
frame2.pack()

value_inside = tk.StringVar(frame1)         # Variable to follow-up
value_inside.set("Home") 
option_list = ["Home", "Position 1", "Position 2", "Position 3", "Position 4"]
give_sequence = tk.OptionMenu(frame2, value_inside, *option_list)
give_sequence.config(font = (font_type, 12), width = 9, anchor = 'center', justify = "center", background = 'white', cursor = "hand2")
give_sequence.grid(row=0, column = 1)

menu = frame2.nametowidget(give_sequence.menuname)
menu.config(font = (font_type, 12), background = 'white')

tk.Label(frame2, text="Position: ", background = background_type, foreground = 'white', font = (font_type, 12)).grid(row=0, column = 0)

# Frame for place the submit button, this button will start the movement sequence
frame3 = tk.Frame(root)
frame3.pack(pady=10)

submit_button = tk.Button(frame3, text = 'Submit', command = move_to_point, font = (font_type, 12), anchor = 'center', width = 19, justify = "center", background = 'white', cursor = "hand2") 
submit_button.pack()

# Frame for show the position joints information in real-time
frame4 = tk.Frame(root, background = background_type)
frame4.pack(pady=10)

tk.Label(frame4, text = "Waist", background = background_type, font = (font_type, 12), justify = "center", foreground = 'white', width = 8).grid(row = 0, column = 1)
tk.Label(frame4, text = "Shoulder", background = background_type, font = (font_type, 12), justify = "center", foreground = 'white', width = 8).grid(row = 0, column = 2)
tk.Label(frame4, text = "Elbow", background = background_type, font = (font_type, 12), justify = "center", foreground = 'white', width = 8).grid(row = 0, column = 3)
tk.Label(frame4, text = "Wrist", background = background_type, font = (font_type, 12), justify = "center", foreground = 'white', width = 8).grid(row = 0, column = 4)
tk.Label(frame4, text = "Gripper", background = background_type, font = (font_type, 12), justify = "center", foreground = 'white', width = 8).grid(row = 0, column = 5)

tk.Label(frame4, text="Position read: ", background = '#65A8E1', font = ("maiandra_gd", 12), foreground = 'white').grid(row = 1, column = 0, sticky = "e") 
tk.Label(frame4, text="Error (E - M): ", background = '#65A8E1', font = ("maiandra_gd", 12), foreground = 'white').grid(row = 2, column = 0, sticky = "e")
read1 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read2 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read3 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read4 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read5 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read6 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read7 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read8 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read9 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read10 = tk.Label(frame4, background = 'white', font = ("maiandra_gd", 12), foreground = 'black', width = 9, text = '0º')
read1.grid(row = 1, column = 1)
read2.grid(row = 1, column = 2)
read3.grid(row = 1, column = 3)
read4.grid(row = 1, column = 4)
read5.grid(row = 1, column = 5)
read6.grid(row = 2, column = 1)
read7.grid(row = 2, column = 2)
read8.grid(row = 2, column = 3)
read9.grid(row = 2, column = 4)
read10.grid(row = 2, column = 5)

# Frame for define the close button for close the GUI
frame5 = tk.Frame(root, background = background_type)
frame5.pack(pady = 10)
close_button = tk.Button(frame5, text = 'Close', command = close_window, font = (font_type, 12), anchor = 'center', width = 19, justify = "center", background = 'white', cursor = "hand2")
close_button.pack()

# Finish GUI configuration
###################################################################################################################################################################################################

# Main function
if __name__ == '__main__':
    try:
        for i in range(5):              # Motor torque set-up
            jointCommand('', joints_IDs[i], 'Torque_Limit', torques[i], 0)
            go_home()                   # The robot starts in home
        listener()
        root.mainloop()
    except:
        print('Not posible connect to robot')
        pass