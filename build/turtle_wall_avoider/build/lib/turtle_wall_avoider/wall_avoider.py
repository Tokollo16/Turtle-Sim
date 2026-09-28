#!/usr/bin/env python3
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Pose


class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')

        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10,
        )
        self.timer = self.create_timer(0.05, self.control_callback)

        self.pose = None
        self.waypoints = (
            (8.5, 8.5),
            (2.5, 8.5),
            (2.5, 2.5),
            (8.5, 2.5),
        )
        self.waypoint_index = 0
        self.safe_min = 1.0
        self.safe_max = 10.0
        self.recovery_active = False

    def pose_callback(self, pose):
        self.pose = pose

    def control_callback(self):
        if self.pose is None:
            return

        command = Twist()
        x = self.pose.x
        y = self.pose.y

        near_wall = (
            x <= self.safe_min
            or x >= self.safe_max
            or y <= self.safe_min
            or y >= self.safe_max
        )

        if near_wall:
            # Turn toward the center until the turtle is safely away from a wall.
            self.recovery_active = True
            target_x, target_y = 5.5, 5.5
        else:
            if self.recovery_active:
                self.recovery_active = False
            target_x, target_y = self.waypoints[self.waypoint_index]

        delta_x = target_x - x
        delta_y = target_y - y
        distance = math.hypot(delta_x, delta_y)
        target_heading = math.atan2(delta_y, delta_x)
        heading_error = self.normalize_angle(target_heading - self.pose.theta)

        if not self.recovery_active and distance < 0.25:
            self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)

        command.angular.z = max(-2.0, min(2.0, 4.0 * heading_error))
        if abs(heading_error) < math.pi / 3:
            command.linear.x = min(2.0, 0.8 * distance)
        else:
            command.linear.x = 0.0

        self.publisher.publish(command)

    @staticmethod
    def normalize_angle(angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def stop(self):
        self.publisher.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    node = WallAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
