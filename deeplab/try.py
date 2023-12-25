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
print(' - cv2.__file__ = ',cv2.__file__)

import rospy
from sensor_msgs.msg import Image as rosImage
from cv_bridge import CvBridge, CvBridgeError
from PIL import Image
global  count
count = 0


def load_model():
    global model, device

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') 
    model = network.deeplabv3plus_mobilenet(num_classes=19, output_stride=16)
    utils.set_bn_momentum(model.backbone, momentum=0.01)
    ckpt = "/home/tarun/Documents/deeplab/model/best_deeplabv3plus_mobilenet_cityscapes_os16.pth"
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
    


def imageCallback(image_msg):
    global device, count
    cv_img = CvBridge().imgmsg_to_cv2(image_msg, "bgr8")
    pil_img = im.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
    #print("Image size for pil_img  :", pil_img.size)


    image_pub = rospy.Publisher("/semantic/image", rosImage, queue_size=10)
    image_pub2 = rospy.Publisher("/masked/image", rosImage, queue_size=10)
    transform = T.Compose([
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225]),
        ])

    with torch.no_grad():
        pil_img = transform(pil_img).unsqueeze(0) # To tensor of NCHW
        pil_img = pil_img.to(device)
         
        pred = model(pil_img).max(1)[1].cpu().numpy()[0] # HW
        #print("size of pred:", pred.size)
        decode_fn = Cityscapes.decode_target
        colorized_preds = decode_fn(pred).astype('uint8')
        #print("size of colorized_preds:", colorized_preds.size)
        colorized_preds = im.fromarray(colorized_preds)
        seg_cv_img = cv2.cvtColor(np.asarray(colorized_preds),cv2.COLOR_RGB2BGR)
        pub_image = CvBridge().cv2_to_imgmsg(seg_cv_img, "bgr8")
        pub_image.header.frame_id = 'camera_link'
        pub_image.header.stamp = rospy.Time.now()
        image_pub.publish(pub_image)
        
        mask = (seg_cv_img[:, :, 0] == 0) & (seg_cv_img[:, :, 1] == 0) & (seg_cv_img[:, :, 2] == 0)

        # Apply the mask to the RGB image
        cv_img[mask] = 0
        # Save the masked RGB image
        
        pub_image2 = CvBridge().cv2_to_imgmsg(cv_img, "bgr8")
        pub_image2.header.frame_id = 'camera_link'
        pub_image2.header.stamp = rospy.Time.now()
        image_pub2.publish(pub_image2)
        
        
        #cv2.imshow("seg_cv_img" , seg_cv_img)
        #cv2.waitKey()
        count = count+1
        print(f"Publishing image number", count)






if __name__ == '__main__':
    rospy.init_node("deeplab_ros")
    load_model()
    image_sub = rospy.Subscriber("/image_conv", rosImage, imageCallback, queue_size=10)
    rospy.spin()

