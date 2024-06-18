FROM osrf/ros:jazzy-simulation
WORKDIR /ws

ADD . src/bittle
RUN apt-get update && apt-get install -y xvfb
RUN rosdep install -y --from-paths src
RUN . /opt/ros/jazzy/setup.sh && colcon build
