# turtle_chaser

A multi-node ROS 2 Humble system in Python. You drive `turtle1` with the keyboard, and an autonomous `turtle2` chases it in real time inside turtlesim.

## Nodes

| Node | What it does |
|---|---|
| `keyboard_teleop` | Reads WASD keys and publishes `geometry_msgs/Twist` on `/turtle1/cmd_vel` |
| `spawner` | Calls the `/spawn` service once to create `turtle2` |
| `chaser` | Subscribes to `/turtle1/pose` and `/turtle2/pose`, and publishes `Twist` on `/turtle2/cmd_vel` using a proportional controller |

## Build

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select turtle_chaser
source install/setup.bash
```

## Run

Open a separate terminal for each (source `install/setup.bash` in every one):

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_chaser spawner
ros2 run turtle_chaser chaser
ros2 run turtle_chaser keyboard_teleop
```

Controls: `w`/`s` forward/backward, `a`/`d` turn left/right, space to stop, `q` to quit.

## How the chaser works

Every 0.05 s it computes the distance and the angle to `turtle1`, normalises the angle error to [-pi, pi], and sends a forward speed proportional to the distance (slowed when not facing the target) and an angular speed proportional to the angle error. It stops when closer than 0.5 units.

## License

Apache-2.0
