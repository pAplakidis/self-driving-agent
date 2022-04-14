#!/usr/bin/env python3
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

from generate_paths import *
from util import *


# TODO: multi-task with pose, lead car, etc
class DrivingModel(nn.Module):
  def __init__(self):
    super(DrivingModel, self).__init__()
    self.path_points = 246  # TODO: some are 246 and some 247 (take min)
  
    # prep resnet18 conv backbone (TODO: maybe use Efficientnet)
    self.backbone = models.resnet18(pretrained=True)
    self.num_feats = self.backbone.fc.in_features
    del self.backbone.fc

    # TODO: this could be an RNN instead!!!
    # prep Linear layers (TODO: maybe use Bayesian)
    self.relu = nn.ReLU()
    self.fc1 = nn.Linear(self.num_feats, 256)
    self.bn1 = nn.BatchNorm1d(256)
    self.fc2 = nn.Linear(256, self.path_points*2)
    self.path_planner = nn.Sequential(self.fc1, self.bn1, self.relu, self.fc2)

  def forward(self, x):
    x = self.backbone(x)
    x = self.path_planner(x)
    return x


def get_train_data():
  pass

def get_val_data():
  pass

def train():
  pass

def eval():
  pass


if __name__ == '__main__':
  print("Hello")
  model = DrivingModel()
  print(model)

