from imutils import paths
from  Blocks.duplicate import Duplicate
class Cleaner():
    def __init__(self,config):
        self.config = config 

    def run(self):
        for filter in self.config['filters']:
            if filter['type'] == 'remove_duplicate':
                Duplicate(filter['args']).run(self.config['input_folder'][0],self.config['output_folder'][0])