import cv2
import numpy as np
import sys
import os
from imutils import paths

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Trainings.network import Net
import torch

#with mask [0,1] , without [1,0]

img_resolution = 96

device = torch.device('cpu')
model = Net()
model.load_state_dict(torch.load(r"Models/0.636#faceVsmask", map_location=device))

def testPhotos():
  # path = input("feed me the full path of the image to test :) : ")
  imagePaths = list(paths.list_images(r"Assets/"))
  for path in imagePaths:
    imgg = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

    img = cv2.resize(imgg,(img_resolution,img_resolution))
    img_array =  np.array(img)
    img_tensor = torch.Tensor(img_array)
    net_output = model(img_tensor.view(-1,1,img_resolution,img_resolution))

    print("masked : ", round(np.exp(net_output[0][1].item()), 3) *100, " %")
    print("without : ", round(np.exp(net_output[0][0].item()), 3) *100, " %")
    print('-------------------------------------------------------------------------')

    cv2.imshow("image", imgg)
    cv2.waitKey(0)

def testFeed():
  vid = cv2.VideoCapture(0)
  while(True):
    _, frame = vid.read()
    imgg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    img = cv2.resize(imgg,(img_resolution,img_resolution))
    img_array =  np.array(img)
    img_tensor = torch.Tensor(img_array)
    net_output = model(img_tensor.view(-1,1,img_resolution,img_resolution))

    # print("masked : ", round(np.exp(net_output[0][1].item()), 3) *100, " %")
    # print("without : ", round(np.exp(net_output[0][0].item()), 3) *100, " %")
    # print('-------------------------------------------------------------------------')
    font = cv2.FONT_HERSHEY_SIMPLEX
  
    # Use putText() method for
    # inserting text on video
    masked = round(np.exp(net_output[0][1].item()), 3) *100
    Nomasked = round(np.exp(net_output[0][0].item()), 3) *100
    cv2.putText(frame, 
                "masked : "+ str(masked)+ " % \n", 
                (30, 50), 
                font, 0.8, 
                (255, 0, 0), 
                2, 
                cv2.LINE_4)
    cv2.putText(frame, 
                "without : "+ str(Nomasked)+ " %", 
                (30, 80), 
                font, 1, 
                (255, 0, 0), 
                2, 
                cv2.LINE_4)
    if(masked > Nomasked):
      cv2.putText(frame, 
                'Masked', 
                (400, 450), 
                font, 1, 
                (0, 255, 0), 
                2, 
                cv2.LINE_4)
    else :
      cv2.putText(frame, 
                "not masked",
                (400, 450), 
                font, 1, 
                (0, 0, 255), 
                2, 
                cv2.LINE_4)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  vid.release()
  cv2.destroyAllWindows()

testFeed()