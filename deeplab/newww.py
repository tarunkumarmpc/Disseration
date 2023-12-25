#!/usr/bin/env python3

from pyexpat import model
import network
import utils
import os
import numpy as np

from datasets import  Cityscapes
from torchvision import transforms as T

import torch
import torch.nn as nn

from PIL import Image as im

import sys
import cv2


from PIL import Image
global  count
count = 0


def load_model():
    global model, device

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 
    model = network.deeplabv3plus_mobilenet(num_classes=19, output_stride=16)
    utils.set_bn_momentum(model.backbone, momentum=0.01)
    ckpt = "/home/tarun/Documents/fastsam/deeplab/model/best_deeplabv3plus_mobilenet_cityscapes_os16.pth"
    if os.path.isfile(ckpt):
        checkpoint = torch.load(ckpt, map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint["model_state"])
        model = nn.DataParallel(model)
        model.to(device)
        print("Resume model from %s" % ckpt)
        del checkpoint
    else:
        print("[!] Retrain")
        model = nn.DataParallel(model)
        model.to(device)
    model = model.eval()
    


if __name__ == '__main__':

    load_model()



