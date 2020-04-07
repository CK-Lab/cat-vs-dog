import os
import argparse
import torch
import torchvision.models as models
import cv2
from PIL import Image
import numpy as np
from torchvision import transforms
from tqdm import tqdm
import models

CLASSES=['cat','dog']

transformsImage = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def get_lastest_model(modeldir="checkpoints"):
    files = os.listdir(modeldir)
    if len(files)==0:
        return None
    files.sort(key=lambda fn:os.path.getmtime(modeldir + "/" + fn))
    lastest = os.path.join(modeldir,files[-1])
    return lastest

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--use_gpu",type=bool,default=True,help='an integer for the accumulator')
    parser.add_argument("--image_dir",type=str,default="../data/test1")
    parser.add_argument("--image_path",type=str,default="../data/test1/1.jpg")
    parser.add_argument("--load_model_path",type=str,default=None)
    parser.add_argument("--model",type=str,default="MnasNet",choices=["MRNet","ResNet50","SqueezeNet","MnasNet"])
    return parser.parse_args()

def test_image(model, device, imgpath):
    img = cv2.imread(imgpath)
    #img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = transformsImage(img).unsqueeze(0)
    outputs = model(image.to(device))
    _, index = torch.max(outputs, 1)
    percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
    print(imgpath,CLASSES[index[0]], percentage[index[0]].item())

def test_dir(model, device, dir):
    files = os.listdir(dir)
    for file in tqdm(files):
        imgpath = dir+'/'+file
        test_image(model,device, imgpath)

@torch.no_grad()
def demo():
    args = get_args()
    model = getattr(models,args.model)()
    if not args.load_model_path:
        args.load_model_path = get_lastest_model()
    if not args.load_model_path:
        print("No pretrained model found")
        return
    m1 = torch.load(args.load_model_path)
    model.load_state_dict(torch.load(args.load_model_path))
    device = torch.device('cpu')
    if args.use_gpu:
        device = torch.device('cuda')
    model.to(device)
    model.eval()
    test_image(model, device, args.image_path)
    #test_dir(model, device, args.image_dir)

if __name__=="__main__":
    demo()