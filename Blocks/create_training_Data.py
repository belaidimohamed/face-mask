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
        self.img_size = 75
        cats = config['input_data'][0]
        dogs = config['input_data'][1]
        self.labels = { dogs:1, cats:0 }
        self.training_data = []
        self.catCount = 0
        self.dogCount = 0
        self.error = 0
    def run(self):
        self.make_training_data()

    def make_training_data(self):
        for label in self.labels :
                print(label)
                f=open(label)
                paths = json.load(f)['clean']
                for path in tqdm(paths):
                    try :
                        img = cv2.imread(path , cv2.IMREAD_GRAYSCALE)
                        img = cv2.resize(img , (self.img_size,self.img_size))
                        # img = C.contour(img)
                        self.training_data.append([np.array(img, dtype="object"), np.eye(2)[self.labels[label]]])
                        if label == self.cats :
                            self.catCount +=1
                        elif label == self.dogs :
                            self.dogCount += 1
                    except Exception as e:
                        self.error+=1
                        pass
        np.random.shuffle(self.training_data)
        np.save(self.config['output_folder'][0] + 'training_data_75.npy',self.training_data)
        print('cats: ',self.catCount)
        print('dogs: ',self.dogCount)
        print('error',self.error)





