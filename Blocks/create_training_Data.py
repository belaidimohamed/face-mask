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
        self.img_size = 50
        self.obj1 = config['input_data'][0] #with mask
        self.obj2 = config['input_data'][1] #without
        self.labels = {  self.obj1:1 , self.obj2:0 }
        self.training_data = []
        self.objCount1 = 0
        self.objCount2 = 0
        self.error = 0
    def run(self):
        self.make_training_data()

    def make_training_data(self):
        for label in self.labels :
                print(label)
                f=open(label)
                paths = json.load(f)['clean']
                for path in tqdm(paths):
                    # try :
                    img = cv2.imread(path , cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img , (self.img_size,self.img_size))
                    # img = C.contour(img)
                    self.training_data.append([np.array(img, dtype="object"), np.eye(2)[self.labels[label]]])
                    if label == self.obj1 :
                        self.objCount1 +=1
                    elif label == self.obj2 :
                        self.objCount2 += 1
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





