# Turtle wall avoider

This ROS 2 Humble package drives `turtle1` around a rectangular route that stays inside the turtlesim window. It uses the turtle pose feedback and includes a center-seeking recovery when the turtle gets close to a wall.

## Build

```bash
cd ~/ROS2
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## Run

In one terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

In another terminal:

```bash
cd ~/ROS2
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run turtle_wall_avoider wall_avoider
```

Stop the controller with `Ctrl+C`; it publishes a zero velocity command before shutting down.
# Turtle-Sim
