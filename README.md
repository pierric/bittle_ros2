[![Build](https://github.com/pierric/bittle_ros2/actions/workflows/docker-image.yml/badge.svg)](https://github.com/pierric/bittle_ros2/actions/workflows/docker-image.yml)

# RUN w/ docker
```
docker build -t bittle-sim .

xhost +local:root

docker run --gpus=all -it --rm \
    -e "DISPLAY=$DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network host \
    --ipc host \
    --env=NVIDIA_VISIBLE_DEVICES=all \
    --env=NVIDIA_DRIVER_CAPABILITIES=all \
    bittle-sim bash
```

Node, nvidia gpu is for accelerating the gazebo sim.
