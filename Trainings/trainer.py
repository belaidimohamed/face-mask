import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from tqdm import tqdm
from Trainings.network import Net
import os
import time
import sys

class Trainer():
  def __init__(self,config):
    if torch.cuda.is_available(): self.device = torch.device("cuda:0") 
    else: self.device = torch.device("cpu")

    self.config = config
    self.img_resolution = 96
    self.net = Net().to(self.device)
    self.optimizer = optim.Adam(self.net.parameters(), lr=0.001)
    self.loss_function = nn.MSELoss()
    # self.loss_function = nn.CrossEntropyLoss()

  
  def run(self) :
    self.splitData() # put numpy data into tensors and flaten them
    self.train()     # train the stupid model
    self.test()      # put the model into a test 


  def splitData(self):
    print("splitting data ...")
    training_data = np.load(self.config['input_data'][0],allow_pickle=True)

    X = torch.Tensor([i[0] for i in training_data]).view(-1,self.img_resolution,self.img_resolution)
    X = X/255.0
    Y = torch.Tensor([i[1] for i in training_data])
    VAL_PCT = 0.1  # lets reserve 10% of our data for validation
    val_size = int(len(X)*VAL_PCT)

    self.train_X = X[:-val_size]
    self.train_y = Y[:-val_size]

    self.test_X = X[-val_size:]
    self.test_y = Y[-val_size:]

    print(len(self.train_X), len(self.test_X))



  def smoothingLabel(self,outputs, target ,smoothing_coefficient) :
      weight = outputs.new_ones(outputs.size()) * smoothing_coefficient / (outputs.size(-1) - 1.)
      target = torch.from_numpy(np.where(target.cpu().numpy() == 1)[1]).to(self.device)
      weight.scatter_(-1, target.unsqueeze(-1), (1. - smoothing_coefficient))
      losses= -weight * outputs
      return losses.sum(dim=-1).mean()

# ------------------------------------------------- Training ----------------------------------------------------

  def train(self,BATCH_SIZE=128,EPOCHS=40):
    print('Starting training process ..')
    optimizer = optim.Adam(self.net.parameters(), lr=0.001)

    for epoch in range(EPOCHS):
        for i in range(0, len(self.train_X), BATCH_SIZE):

            batch_X = self.train_X[i:i+BATCH_SIZE].view(-1, 1, self.img_resolution, self.img_resolution)
            batch_y = self.train_y[i:i+BATCH_SIZE]

            batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
            self.net.zero_grad()

            optimizer.zero_grad()   # zero the gradient buffers
            outputs = self.net(batch_X)

            # loss = self.smoothingLabel(outputs, batch_y,0.12)
            loss = self.loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()    # Does the update

        print(f"Epoch: {epoch}. Loss: {loss}")

# ------------------------------------------------- Tests ----------------------------------------------------


  def test(self):
    self.test_X.to(self.device)
    self.test_y.to(self.device)
    correct = 0
    total = 0
    with torch.no_grad():
        for i in tqdm(range(len(self.test_X))):
            real_class = torch.argmax(self.test_y[i]).to(self.device)
            net_out = self.net(self.test_X[i].view(-1, 1, self.img_resolution, self.img_resolution).to(self.device))[0]  # returns a list,
            predicted_class = torch.argmax(net_out)

            if predicted_class == real_class:
                correct += 1
            total += 1

    print("Accuracy: ", round(correct/total, 3))
    response = input('save me or no (y/n) ? : ')
    while 1:
        if response == 'n':
            break
        elif response == 'y':
            torch.save(self.net.state_dict(), os.path.join(self.config["output_folder"][0],str(round(correct/total, 3))+"#faceVsmask" ))
            print('saving done !')
            break
        else :
            pass








#MSELoss 0.764
#sm = 0.1  0.757







