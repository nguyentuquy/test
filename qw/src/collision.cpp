//include libraries
#include <kobuki_msgs/BumperEvent.h>
#include <geometry_msgs/Twist.h>
#include <ros/ros.h>

//define the bumperCallback function
void bumperCallback(const kobuki_msgs::BumperEvent bumperMessage)
{
  ROS_INFO("bumper hit. value = [%d]", bumperMessage.bumper);
}

//ROS node entry point
int main(int argc, char **argv)
{

  ros::init(argc, argv, "turtlebot_test_node");
  ros::NodeHandle n;

  ros::Subscriber bumperSubscriber = n.subscribe("/mobile_base/events/bumper", 100, bumperCallback);

  ros::Publisher velocityPublisher = n.advertise<geometry_msgs::Twist>("cmd_vel_mux/input/teleop", 1);

  ROS_INFO_STREAM("Ctrl + C to stop me");
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

  while (n.ok()) {
    velocityPublisher.publish(cmd);
    rate.sleep();
  }

  return 0;
}
