from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command

import os
from ament_index_python.packages import get_package_share_path

from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
from launch.event_handlers import OnProcessExit, OnProcessStart



def generate_launch_description():
    
    urdf_path = os.path.join(get_package_share_path('scara_mujoco_description_pkg'),'urdf','scara_trajectory_controller.xacro')
    
    rviz_config_path = os.path.join(get_package_share_path('scara_mujoco_bringup_pkg'),'rviz','scara_trayectory_rviz.rviz')
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description':robot_description}]
    )

    config_arg = DeclareLaunchArgument(name = 'rvizconfig', default_value = rviz_config_path)
    
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    controller_config_file = os.path.join(get_package_share_path('scara_mujoco_description_pkg'), 'config', 'scara_trajectory_controller.yaml')

    node_mujoco_ros2_control = Node(
        package='mujoco_ros2_control',
        executable='mujoco_ros2_control',
        output='screen',
        parameters=[
            {'robot_description':robot_description},
            controller_config_file,
            {'mujoco_model_path':os.path.join(get_package_share_path('scara_mujoco_description_pkg'), 'mujoco_models', 'test_scara.xml')} # aqui es como el world
        ]
    )

    scara_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 
             'scara_trajectory_controller'],
        output='screen'
    )

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen' 
    )
    
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=node_mujoco_ros2_control,
                on_start=[load_joint_state_controller],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[scara_controller],
            )
        ),
        node_robot_state_publisher,
        config_arg,
        rviz2_node,
        node_mujoco_ros2_control,
    ])