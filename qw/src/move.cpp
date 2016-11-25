/*
 * roslaunch turtlebot_gazebo turtlebot_world.launch
 *  $ roslaunch turtlebot_gazebo turtlebot_world.launch
 *  $ rosrun qw move
*/


#include <iostream>
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <stdio.h>

int main(int argc, char** argv)
{
  //init the ROS node
  ROS_INFO_STREAM("Hello World");
  ros::init(argc, argv, "robot_driver"); // init node
  ros::NodeHandle nh;

  //init publisher
  ros::Publisher cmd_vel_pub_;
  cmd_vel_pub_ = nh.advertise<geometry_msgs::Twist>("cmd_vel_mux/input/teleop", 1);

  //init direction that turtlebot should go
  geometry_msgs::Twist base_cmd;
  geometry_msgs::Twist base_cmd_turn_left;

  base_cmd.linear.x = 0;
  base_cmd.linear.y = 0;
  base_cmd.angular.z = 0;
  base_cmd_turn_left.linear.x = 0;
  base_cmd_turn_left.linear.y = 0;
  base_cmd_turn_left.angular.z = 0;


  //and let's go forward by setting X to a positive value
  base_cmd.linear.x = 0.25;
  base_cmd.angular.z = 0.0;
  ROS_INFO_STREAM("And Crashing ... ctrl + c to stop me :)");

  //base_cmd_turn_left will be used to turn turtlebot 90 degrees
  base_cmd_turn_left.linear.x = 0; //m/s
  base_cmd_turn_left.angular.z = 1.57/2; //45 deg/s * 2 sec = 90 degrees

  ros::Rate rate(5); // 5Hz

  while(nh.ok()) { //have we ctrl + C?  If no... keep going!
    //"publish" sends the command to turtlebot to keep going

    //go forward for 2 seconds
    for(int n=10; n>0; n--) {
      cmd_vel_pub_.publish(base_cmd);
      rate.sleep();
    }

    //turn 90 degrees (takes 2 seconds)
    for(int n=10; n>0; n--) {
      cmd_vel_pub_.publish(base_cmd_turn_left);
      rate.sleep();
    }
  }


  base_cmd.linear.x = 0;
  base_cmd.linear.y = 0;
  base_cmd.angular.z = 0;
  cmd_vel_pub_.publish(base_cmd);

  ROS_INFO("Finished\n");

  return 0;
}
