import sys
import termios
import tty
import select

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

HELP = """
Control turtle1:
  w / s : forward / backward
  a / d : turn left / right
  space : stop
  q     : quit
"""


class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.lin_speed = 2.0
        self.ang_speed = 2.0

    def send(self, lin, ang):
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)


def get_key(settings, timeout=0.1):
    tty.setraw(sys.stdin.fileno())
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    key = sys.stdin.read(1) if ready else ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    settings = termios.tcgetattr(sys.stdin)
    print(HELP)

    try:
        while rclpy.ok():
            key = get_key(settings)
            if key == 'w':
                node.send(node.lin_speed, 0.0)
            elif key == 's':
                node.send(-node.lin_speed, 0.0)
            elif key == 'a':
                node.send(0.0, node.ang_speed)
            elif key == 'd':
                node.send(0.0, -node.ang_speed)
            elif key == ' ':
                node.send(0.0, 0.0)
            elif key == 'q' or key == '\x03':  # q or Ctrl+C
                break
    finally:
        node.send(0.0, 0.0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
