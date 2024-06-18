import rclpy
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import Float64MultiArray

pi = 3.14


def controller(node):
    pub = node.create_publisher(
        Float64MultiArray, "/position_controller/commands", 10
    )
    msg = Float64MultiArray()

    def _callback():
        msg.data = [
            pi / 6,
            pi / 6,
            pi / 6,
            pi / 6,
            -pi / 6,
            -pi / 6,
            -pi / 6,
            -pi / 6,
        ]
        pub.publish(msg)

    timer = node.create_timer(0.1, _callback)
    rclpy.spin(node)


if __name__ == "__main__":
    rclpy.init()
    node = rclpy.create_node("bittle_controller")
    try:
        controller(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
