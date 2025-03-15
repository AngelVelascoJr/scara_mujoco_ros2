cmake_minimum_required(VERSION 3.8)
project(scara_mujoco_bringup_pkg)

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
DIRECTORY launch rviz src
DESTINATION share/${PROJECT_NAME}/
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables #They must start with the shebag tag
install(PROGRAMS
  ${PROJECT_NAME}/multi_tray.py
  DESTINATION lib/${PROJECT_NAME} 
)



ament_package()
