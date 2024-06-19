import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    ExecuteProcess,
    RegisterEventHandler,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Package Directories
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")
    pkg_bittle = get_package_share_directory("bittle")

    # Parse robot description from xacro
    robot_description_file = os.path.join(pkg_bittle, "model", "bittle.urdf")
    robot_description_config = xacro.process_file(robot_description_file)

    # Robot state publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[
            {"use_sim_time": True},
            {"robot_description": robot_description_config.toxml()},
        ],
    )

    # Gazebo Sim
    world = os.path.join(pkg_bittle, "model", "world.sdf")
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": f"-r {world}"}.items(),
    )

    # Spawn
    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        parameters=[
            {
                "world": "empty",
                "name": "bittle",
                "topic": "robot_description",
                "z": 10.0,
            }
        ],
        output="screen",
    )

    # Gz - ROS Bridge
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/world/empty/model/bittle/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model",
        ],
        remappings=[
            ("/world/empty/model/bittle/joint_state", "joint_states"),
        ],
        output="screen",
    )

    # Joint controller
    load_joint_controller = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "position_controller",
            #"joint_trajectory_controller",
        ],
        output="screen",
    )

    # RViz
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(pkg_bittle, "config", "joint_states.rviz"),
        ],
    )

    return LaunchDescription(
        [
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=spawn,
                    on_exit=[load_joint_controller],
                )
            ),
            gazebo,
            spawn,
            bridge,
            robot_state_publisher,
            rviz,
        ]
    )
