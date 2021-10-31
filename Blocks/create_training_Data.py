import os
import cv2
from tqdm import tqdm
import numpy as np
import json
#object1 [0,1] , object2 [1,0]

REBUILD_DATA = True
class CreateData:
    def __init__(self,config):
        self.config = config 
        self.img_size = 96
        self.obj1 = config['input_data'][0] #with mask [0,1]
        self.obj2 = config['input_data'][1] #without [1,0]
        self.labels = {  self.obj1:1 , self.obj2:0 }
        self.training_data = []
        self.objCount1 = 0
        self.objCount2 = 0
        self.error = 0
    def run(self):
        self.make_training_data()
    def getMinNumber(self):
        l = []
        for label in self.labels :
            f=open(label)
            l.append(len(json.load(f)['clean']))
        return min(l)

    def make_training_data(self):
        min = self.getMinNumber()
        for label in self.labels :
                print(label)
                f=open(label)
                paths = json.load(f)['clean']
                for path in tqdm(paths):
                    # try :
                    img = cv2.imread(path , cv2.IMREAD_GRAYSCALE)
                    cv2.imshow("image", img)
                    cv2.waitKey(10)
                    img = cv2.resize(img , (self.img_size,self.img_size))
                    # img = C.contour(img)
                    self.training_data.append([np.array(img, dtype="object"), np.eye(2)[self.labels[label]]])
                    if label == self.obj1 :
                        self.objCount1 +=1
                        # if(self.objCount1 > min +20):
                        #     break
                    elif label == self.obj2 :
                        self.objCount2 += 1
                        # if(self.objCount2 > min +20):
                        #     break
                    # except Exception as e:
                    #     self.error+=1
                    #     pass
        np.random.shuffle(self.training_data)
        try:
            np.save(os.path.join(self.config['output_folder'][0] , 'training_data.npy'),self.training_data)
        except :
            os.mkdir(self.config['output_folder'][0])
            np.save(os.path.join(self.config['output_folder'][0] , 'training_data.npy'),self.training_data)

        print('with mask: ',self.objCount1)
        print('without mask: ',self.objCount2)
        print('error',self.error)





