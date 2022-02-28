# Self Driving Agent
A toy implementation of an autonomous driving agent for self-driving cars (inspired by comma.ai's Openpilot)

## TODO
- implement a localizer (EKF, using visual odometry, GPS, IMU, etc), also used for autolabeling path planning
- comma2k19 dataset (video, GPS, IMU, CAN bus stuff)
- for the multi-task net: 2 frames => model (ResNet, RNN) => path(s) + pose + lead car
- path => path planner => controls (PID loop)
- lateral + logitudinal planning handled by net
- ROS2 or Cereal for messaging between daemon processes
- CARLA simulator for testing

