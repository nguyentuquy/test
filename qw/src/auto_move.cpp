/*
 * roslaunch turtlebot_gazebo turtlebot_world.launch
 *  $ roslaunch turtlebot_gazebo turtlebot_world.launch
 *  $ rosrun qw move
*/

#include <iostream>
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <kobuki_msgs/BumperEvent.h>
#include <sensor_msgs/LaserScan.h>

void bumperCallback(const kobuki_msgs::BumperEvent bumperMessage)
{
  ROS_INFO("bumper hit. value = [%d]", bumperMessage.bumper);
}

int main(int c, char ** v){
  ros::init(c,v, "auto_move");
  ros::NodeHandle node_handle;

  ros::Publisher pub = node_handle.advertise<geometry_msgs::Twist>("cmd_vel_mux/input/teleop", 1);


  ros::Subscriber sub = node_handle.subscribe("/mobile_base/events/bumper",100, bumperCallback);

  //init direction that turtlebot should go
  geometry_msgs::Twist cmd;
  geometry_msgs::Twist cmd_turn_left;

  cmd.linear.x = 0;
  cmd.linear.y = 0;
  cmd.angular.z = 0;

  cmd_turn_left.linear.x = 0;
  cmd_turn_left.linear.y = 0;
  cmd_turn_left.angular.z = 0;

  cmd.linear.x = 0.25;
  cmd.linear.y = 0;

  ROS_INFO_STREAM("Ctrl + C to stop me");
  cmd_turn_left.linear.x = 0;
  cmd_turn_left.angular.z = 10;

  ros::Rate rate(5);

  while (node_handle.ok()) {
    pub.publish(cmd);
    rate.sleep();

//    pub.publish(cmd_turn_left);
//    rate.sleep();
  }



}
