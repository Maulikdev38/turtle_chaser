import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn


class Spawner(Node):
    def __init__(self):
        super().__init__('spawner')
        self.client = self.create_client(Spawn, '/spawn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn service...')

    def spawn(self):
        req = Spawn.Request()
        req.x = 2.0
        req.y = 2.0
        req.theta = 0.0
        req.name = 'turtle2'
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    node = Spawner()
    result = node.spawn()
    node.get_logger().info(f'Spawned {result.name}')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
