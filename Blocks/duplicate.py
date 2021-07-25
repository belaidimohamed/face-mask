import cv2
import numpy as np
from imutils import paths
import json
import os

class Duplicate():
	def __init__(self,config={}):
		self.config = config 
		self.cleaned = {'removed':0,'rest':0,'clean':[]}
		self.all = 0
	def dhash(self,image, hashSize=8):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		resized = cv2.resize(gray, (hashSize + 1, hashSize))
		diff = resized[:, 1:] > resized[:, :-1]
		return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
	def hashImages(self,path):
		print("[INFO] computing image hashes...")
		imagePaths = list(paths.list_images(path))
		self.all = len(imagePaths)
		hashes = {}
		for imagePath in imagePaths:
			image = cv2.imread(imagePath)
			h = self.dhash(image)
			p = hashes.get(h, [])
			p.append(imagePath)
			hashes[h] = p
		return hashes
	def run(self, pathIn,pathOut):
		hashes = self.hashImages(pathIn)
		if not os.path.isdir(pathOut):
			os.mkdir(pathOut)
		for (h, hashedPaths) in hashes.items():
			if len(hashedPaths) > 1:
				montage = None
				for p in hashedPaths:
					image = cv2.imread(p)
					image = cv2.resize(image, (150, 150))
					if montage is None:
						montage = image
					else:
						montage = np.hstack([montage, image])
				print("[INFO] hash: {}".format(h))
				cv2.imshow("Montage", montage)
				cv2.waitKey(20)
				self.cleaned['removed'] += len(hashedPaths[1:])
				self.cleaned['clean'].append(hashedPaths[0])
			else :
				self.cleaned['clean'].append(hashedPaths[0])
		self.cleaned['rest'] = self.all - self.cleaned['removed']
		print('{} % of images have been deleted. \nRest= {} , Removed = {}'.format( 
			(self.cleaned['removed'] /self.all)*100,
			 self.cleaned['rest'],
			 self.cleaned['removed']))
		with open(os.path.join(pathOut,'duplicate_clean.json'), 'w') as fp:
			json.dump(self.cleaned, fp,indent=4)