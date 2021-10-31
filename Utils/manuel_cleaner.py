import json
import cv2
import os
from tqdm import tqdm

class ManuelCleaner():
    def __init__(self):
        self.input_file = r'Data/clean_Nomask/duplicate_clean.json' 
        self.output_file = r'Data/clean_Nomask/manuel_clean.json'
        try:
          f = open(self.output_file)
          self.cleaned = json.load(f)
        except:
          self.cleaned = {'clean':[],'lastPosition':0 , 'removed':0}
    def run(self):
      f = open(self.input_file)
      x= self.cleaned['lastPosition']
      paths = json.load(f)['clean'][x:]
      
      for i in  tqdm(range(len(paths))) :
        while 1:
          img = cv2.imread(paths[i])
          cv2.imshow("Save : Y or N", img)
          x = cv2.waitKey(0)
          if x == ord('n'):
            self.cleaned['removed'] += 1
            break
          elif x == ord('y'):
            self.cleaned['clean'].append(paths[i])
            break
          elif x == ord('q'):
            with open(os.path.join('Data/clean_Nomask/','manuel_clean.json'), 'w') as fp:
              json.dump(self.cleaned, fp,indent=4)
            exit()
        self.cleaned['lastPosition'] +=1

man = ManuelCleaner()
man.run()