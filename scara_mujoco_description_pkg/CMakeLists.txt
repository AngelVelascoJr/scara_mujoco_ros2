cmake_minimum_required(VERSION 3.8)
project(scara_mujoco_description_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(mujoco_ros2_control REQUIRED)

install(
  DIRECTORY launch rviz urdf config mujoco_models
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
