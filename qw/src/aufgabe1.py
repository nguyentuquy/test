#!/usr/bin/env python
import rospy
import sys
import math

from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from random import random

def argmin(array):
    value = 10.0
    index = 0
    rospy.loginfo("array size"+ 'len(array)')
    for i in range(len(array)):
        if not math.isnan(array[i]):
            if array[i]<value:
                value=array[i]
                index = i
    return index
    
def on_bumper(data):
    # Bumper was hit
    global bumper
    roundCounter = 0
    if data.state==1:
        bumper = True


def on_scan(data):
    global actual
    global angle_increment
    global angle_min
    global nearest
    global twist
    global publisher
    global right
    global left
    global front
    global bumper

    if (actual % 30 == 0):
        actual = 0
        if not math.isnan(data.ranges[len(data.ranges)-1]):
            right = data.ranges[0]
        else: 
            right = 0

        if not math.isnan(data.ranges[0]):
            left = data.ranges[len(data.ranges)-1]
        else: 
            left = 0

        if not math.isnan(data.ranges[len(data.ranges)/2]):
            front = data.ranges[len(data.ranges)/2]
        else: 
            front = 0
        rospy.loginfo(front)
        rospy.loginfo(left)
        rospy.loginfo(right)

        if bumper == False:
              if (0<front<=0.9 and 0<right<=0.9) or (0<front<=0.9 and left>0.9) :       
                  driveLeft()
              elif (0<front<=0.9 and right>0.9)or(0<front<=0.9 and 0<left<=0.9):
                   driveRight()
              elif (0<front<=0.9 and right>0.9 and left>0.9 and right>left):
                   driveRight()
              elif (0<front<=0.9 and right>0.9 and left>0.9 and right<left):
                    driveLeft()
              elif (front>0.9 or front==0) and  (right>0.9 or 0<left<0.9):
                   bitRight()
                   
              elif (front>0.9 or front==0) and (0<right<0.9 or left>0.9):
                   bitLeft()
              elif (front>0.9 or front==0) and 0<right<0.9 and 0<left<0.9 and right>left :
                   driveRight()
              elif (front>0.9 or front==0) and 0<right<0.9 and 0<left<0.9 and right<left :
                   driveLeft()
              #else:
                  #driveOn() 
                 
              
        else:
             bumper = False 
             driveBack()
    actual = actual + 1  
                      

    
def frontDetect():
    global twist
    global rate
    global publisher
    rospy.loginfo("Front detected")
    twist = Twist()
    twist.linear.x = 0.00;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = 0.08	;
    publisher.publish(twist)
    rate.sleep()

def driveRight():
    global twist
    global rate
    global publisher
    rospy.loginfo("Drive right")
    twist = Twist()
    twist.linear.x = 0.00;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = -0.08;
    publisher.publish(twist)     
    rate.sleep()  
def driveLeft():
    global twist
    global rate
    global publisher
    rospy.loginfo("Drive left")
    twist = Twist()
    twist.linear.x = 0.00;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = 0.08;
    publisher.publish(twist)     
    rate.sleep()  
def bitRight():
    global twist
    global rate
    global publisher
    rospy.loginfo("Drive a bit right")
    twist = Twist()
    twist.linear.x =0.05;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = -0.05;
    publisher.publish(twist)
    rate.sleep()

def bitLeft():
    global twist
    global rate
    global publisher
    rospy.loginfo("Drive a bit left")       
    twist = Twist()
    twist.linear.x = 0.05;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = 0.05;
    publisher.publish(twist)
    rate.sleep()

def driveOn():
    global twist
    global rate
    global publisher   
    rospy.loginfo("Drive on")
    twist = Twist()
    twist.linear.x =0.1;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = 0;
    publisher.publish(twist)
    rate.sleep()

def driveBack():
    global twist
    global rate
    global publisher      
    rospy.loginfo("Drive back")
    twist = Twist()
    twist.linear.x = -0.1;                   # our forward speed
    twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!        
    twist.angular.x = 0; twist.angular.y = 0;   #          or these!
    twist.angular.z = 0;
    publisher.publish(twist)
    rate.sleep()


def listener():
    # listen to bumper events
    global publisher 
    publisher = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1) 
    rospy.Subscriber("/scan", LaserScan, on_scan)
    rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, on_bumper)

def myhook():
    # shutdown hook stop robot
    global twist
    twist=Twist()
    publisher.publish(twist)


    
if __name__ == '__main__':
    # init node
    rospy.init_node('mazerun', anonymous=True)
    rospy.on_shutdown(myhook)
    listener()
    # global variable indicating a bumper hit (e.g. a wall)
    global twist
    global actual
    global angle_increment
    global angle_min
    global nearest
    global publisher
    global right
    global left
    global front
    global bumper
    global rate
    right = 0 
    left = 0
    front = 0
    actual = 0
    counter = 0
    nearest = 10
    backdrive = False
    bumperhit = False
    bumperrelease = True
    bumper = False
    
    # adjust publish rate
    rate=rospy.Rate(5) # rate in Hertz 10 Hertz 100ms

    # short sleep to get started
    rospy.sleep(1) 

    # move forward
    publisher = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1) 


    twist = Twist()
    # move until shtudown isn't called 
    while not rospy.is_shutdown():   
       # i = 5
        #i = i + 1
        #if i > 10:
           # i = 0
          publisher.publish(twist)
          rospy.sleep(0.1)
    # stop robot after bumper hit
    #twist=Twist()
    #publisher.publish(twist)
    
