import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class Chaser(Node):
    def __init__(self):
        super().__init__('chaser')

        self.target_pose = None
        self.my_pose = None

        self.create_subscription(Pose, '/turtle1/pose', self.target_cb, 10)
        self.create_subscription(Pose, '/turtle2/pose', self.my_cb, 10)
        self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.timer = self.create_timer(0.05, self.control_loop)

        self.kp_lin = 1.5
        self.kp_ang = 4.0
        self.max_lin = 3.0
        self.stop_dist = 0.5

    def target_cb(self, msg):
        self.target_pose = msg

    def my_cb(self, msg):
        self.my_pose = msg

    def control_loop(self):
        if self.target_pose is None or self.my_pose is None:
            return

        dx = self.target_pose.x - self.my_pose.x
        dy = self.target_pose.y - self.my_pose.y
        distance = math.hypot(dx, dy)
        desired_angle = math.atan2(dy, dx)

        error = desired_angle - self.my_pose.theta
        error = math.atan2(math.sin(error), math.cos(error))

        cmd = Twist()
        if distance > self.stop_dist:
            speed = min(self.kp_lin * distance, self.max_lin)
            cmd.linear.x = speed * max(0.0, math.cos(error))
            cmd.angular.z = self.kp_ang * error
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = Chaser()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
