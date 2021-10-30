import cv2
import numpy as np
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Trainings.network import Net
import torch

#with mask [0,1] , without [1,0]

img_resolution = 96

device = torch.device('cpu')
model = Net()
model.load_state_dict(torch.load(r"Models/0.619#faceVsmask", map_location=device))

# path = input("feed me the full path of the image to test :) : ")
# path = r'Assets/face2.jpeg'
path = r'Assets/nomask.jpg'
imgg = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

# if imgg == None :
#     imgg = cv2.imread(os.path.join(r"C:\Users\mohamed\Desktop\tensor\assets",path),cv2.IMREAD_GRAYSCALE)

img = cv2.resize(imgg,(img_resolution,img_resolution))
img_array =  np.array(img)
img_tensor = torch.Tensor(img_array)
net_output = model(img_tensor.view(-1,1,img_resolution,img_resolution))

print(net_output[0])
print(torch.argmax(net_output[0]))
# p = torch.softmax(net_output,dim=1)
# print(p)
#
# print("dog : ", round(p[0][1].item(),3) *100 ," %")
# print("cat : ", round(p[0][0].item(),3) *100 ," %")

print("masked : ", round(np.exp(net_output[0][1].item()), 3) *100, " %")
print("without : ", round(np.exp(net_output[0][0].item()), 3) *100, " %")

cv2.imshow("image", imgg)
cv2.waitKey(0)