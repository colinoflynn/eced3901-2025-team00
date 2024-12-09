# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from nav_msgs.msg import Odometry

# http://docs.ros.org/en/noetic/api/geometry_msgs/html/index-msg.html
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist


class NavigateSquare(Node):

    def __init__(self):
        #This calls the initilization function of the base Node class
        super().__init__('navigate_square')

        # We can either create variables here by declaring them
        # as part of the 'self' class, or we could declare them
        # earlier as part of the class itself. I find it easier
        # to declare them here

        # Ensure these are obviously floating point numbers and not
        # integers (python is loosely typed)
        self.x_vel = 0.2
        self.x_now = 0.0
        self.x_init = 0.0
        self.y_now = 0.0
        self.y_init = 0.0
        self.d_now = 0.0
        self.d_aim = 1.0

        # Subscribe to odometry
        self.sub_odom = self.create_subscription(
            Odometry, #Matches the import at the top (nav_msgs.msg import Odometry)
            'odom', #odom topic
            self.odom_callback, #Call this function
            10) #Queue size 10

        # Publish to telocity
        self.pub_vel = self.create_publisher(
            Twist, #Expects the twist message format
            'cmd_vel',
            10) #Queue size 10

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info(f'Timer hit')

        msg = Twist()
        # This has two fields:
        # msg.linear.x
        # msg.angular.z
        	
		# Calculate distance travelled from initial
        self.d_now = pow( pow(self.x_now - self.x_init, 2) + pow(self.y_now - self.y_init, 2), 0.5 )
		
	    # Keep moving if not reached last distance target
        if self.d_now < self.d_aim:
            msg.linear.x = self.x_vel
            msg.angular.z = 0.0
            self.pub_vel.publish(msg)
            self.get_logger().info("Sent: " + str(msg))
        else:
            msg.linear.x = 0.0 # //double(rand())/double(RAND_MAX); //fun
            msg.angular.z = 0.0 # //2*double(rand())/double(RAND_MAX) - 1; //fun
            self.pub_vel.publish(msg)

    def odom_callback(self, msg):
        self.get_logger().info('Msg Data: "%s"' % msg)        
        self.x_now = msg.pose.pose.position.x
        self.y_now = msg.pose.pose.position.y


def main(args=None):
    rclpy.init(args=args)

    navigate_square = NavigateSquare()

    rclpy.spin(navigate_square)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    navigate_square.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
