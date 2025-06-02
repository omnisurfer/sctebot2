from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, PathJoinSubstitution
from launch.substitutions.launch_configuration import LaunchConfiguration

from launch_ros.actions import Node

ARGUMENTS = [
    DeclareLaunchArgument('model', default_value='standard', choices=['standard', 'lite'], description='Sctebot2 Model'),
    DeclareLaunchArgument('use_sim_time', default_value='false', choices=['true', 'false'], description='use_sim_time'),
    DeclareLaunchArgument('robot_name', default_value='sctebot2', description='Robot Name'),
    DeclareLaunchArgument('namespace', default_value=LaunchConfiguration('robot_name'), description='Robot namespace')
]

def generate_launch_description():
    pkg_sctebot2_description = get_package_share_directory('sctebot2_description')

    xacro_file = PathJoinSubstitution(
        [pkg_sctebot2_description, 'urdf', LaunchConfiguration('model'), 'sctebot2.urdf.xacro']
    )

    namespace = LaunchConfiguration('namespace')
    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'robot_description': Command([
                'xacro', ' ', xacro_file, ' ',
                'gazebo:=ignition', ' ',
                'namespace:=', namespace])},
        ],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static')
        ]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[
            ('/tf', 'tf'),
            ('tf_statuc', 'tf_static')
        ]
    )

    # define LaunchDescription variable
    launch_description = LaunchDescription(ARGUMENTS)

    # add nodes to LaunchDescription
    launch_description.add_action(robot_state_publisher)
    launch_description.add_action(joint_state_publisher)

    return launch_description