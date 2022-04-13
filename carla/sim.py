#!/usr/bin/env python3
import random
import glob
import sys
import os
import time
import cv2
import numpy as np

"""
try:
    sys.path.append(glob.glob('/opt/carla-simulator/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'linux-x86_64'))[0])
except IndexError as e:
  print("index error", e)
"""

import carla

IMG_WIDTH = 640
IMG_HEIGHT = 480

actor_list = []

def process_img(img):
  img = np.array(img.raw_data)
  img = img.reshape((IMG_HEIGHT, IMG_WIDTH, 4))
  img = img[:, :, :3]
  cv2.imshow("frame", img)
  cv2.waitKey(1)
  return img/255.0

# TODO: get camera data, GPS, IMU
def carla_main():
  # setup
  client = carla.Client('localhost', 2000)
  client.set_timeout(2.0)  # seconds
  world = client.get_world()
  world.set_weather(carla.WeatherParameters.ClearSunset)
  print(world.get_weather)
  bp_lib = world.get_blueprint_library()

  # spawn a car
  vehicle_bp = bp_lib.filter('vehicle.tesla.*')[1]
  spawn_point = random.choice(world.get_map().get_pawn_points())
  vehicle = world.spawn_actor(vehicle_bp, spawn_point)

  # temp controls
  #vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
  vehicle.set_autopilot(True)

  actor_list.append(vehicle)

  # spawn camera
  camera_bp = bp_lib.find('sensor.camera.rgb')
  camera_bp.set_attribute('image_size_x', f'{IMG_WIDTH}')
  camera_bp.set_attribute('image_size_y', f'{IMG_HEIGHT}')
  blueprint.set_attribute('fov', '110')

  spawn_point  = carla.Transform(carla.Location(x=2.5, z=0.7))
  camera = world.spawn_actor(camera_bp, spawn_point, attach_to=vehicle)
  actor_list.append(vehicle)

  camera.listen(lambda img: process_img(img))
  time.sleep(5)


if __name__ == '__main__':
  print("Hello")
  try:
    carla_main()
  finally:
    print("destroying all actors")
    for a in actor_list:
      a.destroy()
    print('done')

