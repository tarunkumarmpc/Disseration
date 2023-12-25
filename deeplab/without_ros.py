import os
import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms as T
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from datasets import Cityscapes
import network
import utils
from ultralytics import YOLO
import pdb

# Global variables
global count
count = 0

# Initialize a dictionary to store the label counts
label_counts = {'car': 0, 'truck': 0, 'person': 0, 'motorcycle': 0, 'bicycle': 0, 'bus': 0}

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

class CustomDataset:
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = os.listdir(data_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = os.path.join(self.data_dir, self.images[idx])
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        return image

def process_image(image):
    global device, count, label_counts, model_yolo
    counts = {'car': 0, 'truck': 0, 'person': 0, 'motorcycle': 0, 'bicycle': 0, 'bus': 0}

    results = model_yolo(image)
    class_list = results[0].boxes.cls.cpu().numpy()
    counts['car'] = np.sum(results[0].boxes.cls.cpu().numpy() == 2)
    counts['truck'] = np.sum(results[0].boxes.cls.cpu().numpy() == 8)
    counts['person'] = np.sum(results[0].boxes.cls.cpu().numpy() == 0)
    counts['motorcycle'] = np.sum(results[0].boxes.cls.cpu().numpy() == 3)
    counts['bicycle'] = np.sum(results[0].boxes.cls.cpu().numpy() == 1)
    counts['bus'] = np.sum(results[0].boxes.cls.cpu().numpy() == 5)

    transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    with torch.no_grad():
        image = transform(image).unsqueeze(0)
        image = image.to(device)

        pred = model(image)
        pred = pred.squeeze(0).cpu().numpy()

        pred_class = np.argmax(pred, axis=0)

        for label in counts.keys():
            label_counts[label] += counts[label]

        count = count + 1
        print(f"Processing image number {count}")

if __name__ == '__main__':
    load_model()
    data_dir = "/home/tarun/Documents/diss_deepvo/DeepVO-pytorch/DeepVO-pytorch-master/KITTI/images/04"
    custom_dataset = CustomDataset(data_dir)

    

    model_yolo = YOLO('yolov8n.pt')
    for image in custom_dataset:
        process_image(image)

        

    for label_name, count in label_counts.items():
        print(f"Total count of {label_name}: {count}")

    labels = list(label_counts.keys())
    counts = list(label_counts.values())
    plt.bar(labels, counts)
    plt.title('Total Label Counts')
    plt.xlabel('Labels')
    plt.ylabel('Count')
    plt.show()

