import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSHistoryPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from sensor_msgs.msg import PointCloud2

import ros2_numpy as rnp


class Listener(Node):
    def __init__(self):
        super().__init__("t_pc_sub")
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=1,
        )
        self.sub = self.create_subscription(
            PointCloud2, "/camera/camera/depth/color/points", self.callback, qos_profile
        )
        self.pub = self.create_publisher(PointCloud2, "test/points_out", qos_profile)

    def callback(self, msg: PointCloud2):
        np_cloud = rnp.point_cloud2.pointcloud2_to_xyz_rgb(msg)
        xyz, rgb = np_cloud["xyz"], np_cloud["rgb"]
        out_msg = rnp.point_cloud2.xyz_rgb_to_pointcloud2(
            xyz, rgb, frame_id=msg.header.frame_id
        )
        self.pub.publish(out_msg)


def main(args=None):
    rclpy.init(args=args)

    listener = Listener()

    rclpy.spin(listener)

    listener.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
