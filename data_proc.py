#!/usr/bin/env python3
import os
import sys
import cv2
import scipy
import numpy as np
from math import pi

import utils.orientation as orient
import utils.coordinates as coord
from utils.camera import img_from_device, denormalize, view_frame_from_device_frame
from utils.framereader import FrameReader

# TODO: get path points and create a custom log_file for the path_planner

def draw_path(device_path, img, width=1, height=1.2, fill_color=(128, 0, 255), line_color=(0, 255, 0)):
  device_path_l = device_path + np.array([0, 0, height])
  device_path_r = device_path + np.array([0, 0, height])
  device_path_l[:, 1] -= width
  device_path_r[:, 1] += width

  img_points_norm_l = img_from_device(device_path_l)
  img_points_norm_r = img_from_device(device_path_r)
  img_pts_l = denormalize(img_points_norm_l)
  img_pts_r = denormalize(img_points_norm_r)

  # filter out things rejected along the way
  valid = np.logical_and(np.isfinite(img_pts_l).all(axis=1), np.isfinite(img_pts_r).all(axis=1))
  img_pts_l = img_pts_l[valid].astype(int)
  img_pts_r = img_pts_r[valid].astype(int)

  for i in range(1, len(img_pts_l)):
    u1, v1, u2, v2 = np.append(img_pts_l[i-1], img_pts_r[i-1])
    u3, v3, u4, v4 = np.append(img_pts_l[i], img_pts_r[i])
    pts = np.array([[u1,v1],[u2,v2],[u4,v4],[u3,v3]], np.int32).reshape((-1,1,2))
    cv2.fillPoly(img, [pts], fill_color)
    cv2.polylines(img, [pts], True, line_color)


if __name__ == '__main__':
  data_path = "data/5/"
  video_path = "data/5/video.hevc"

  # load log data to construct a path
  frame_times = np.load(data_path + "global_pose/frame_times")
  frame_positions = np.load(data_path + "global_pose/frame_positions")
  frame_orientations = np.load(data_path + "global_pose/frame_orientations")
  euler_angles_ned_deg = (180/pi)*orient.ned_euler_from_ecef(frame_positions[0], orient.euler_from_quat(frame_orientations))

  fr = FrameReader(data_path + "video.hevc")
  for i in range(600):
    # convert the frame_positions to the frame defined by the pose of the first frame
    ecef_from_local = orient.rot_from_quat(frame_orientations[i])
    local_from_ecef = ecef_from_local.T
    frame_positions_local = np.einsum('ij,kj->ki', local_from_ecef, frame_positions - frame_positions[i])

    # show the path
    #img = cv2.imread(data_path + 'preview.png')
    img = fr.get(i, pix_fmt='rgb24')[0]
    draw_path(frame_positions_local[10:250], img)
    cv2.imshow('path', img)
    cv2.waitKey(1)

