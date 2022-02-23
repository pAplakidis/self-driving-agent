#!/usr/bin/env python3
import carla

def carla_main():
  # setup
  client = carla.Client('localhost', 2000)
  client.set_timeout(10.0)  # seconds
  world = client.get_world()
  print(client.get_available_maps())
  world = client.load_world('Town01')

  weather = carla.WeatherParameters(cloudiness=80.0,
                                    precipitation=30.0,
                                    sun_altitude_angle=70.0)
  world.set_weather(weather)
  print(world.get_weather)

  bp_lib = world.get_blueprint_library()
  world_map = world.get_map()

  # spawn a car
  vehicle_bp = blueprint_library.filter('vehicle.tesla.*')[1]


if __name__ == '__main__':
  print("Hello")

