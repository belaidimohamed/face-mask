from argparse import ArgumentParser
import yaml
from Download.smart_downloader import SmartDownloader
from Blocks.cleaner import Cleaner
from Blocks.create_training_Data import CreateData

class AI_pipeline():
    def __init__(self,config):
        self._config = config

    def run(self,steps):
        for step in steps:
            if step=="download":
                self._downloader = SmartDownloader(self._config[step.capitalize()])
                self._downloader.crowl()
            if step=="clean":
                self._cleaner = Cleaner(self._config[step.capitalize()])
                self._cleaner.run()
            if step=="create":
                self._createData = CreateData(self._config[step.capitalize()])
                self._createData.run()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("config", help="yaml config defining the training pipleline", type=str)
    parser.add_argument("--download", help="Run download module",action='store_true')
    parser.add_argument("--clean", help="Flag images to be cleaned into a json file . Then delete this images in the output folder",action='store_true')
    parser.add_argument("--create", help="create a numpy dataset out of the cleaned data",action='store_true')
    args = parser.parse_args()

    config_file_path = getattr(args, 'config', False)

    with open(config_file_path,encoding='utf8') as f:
        config = yaml.safe_load(f)


    steps=[k for k,v in vars(args).items() if v==True] # get the --keys in arguments
    if not steps : # if the user is too stupid to give args we will get it for him
        steps=[k.lower() for k in config.keys()]
    AIP = AI_pipeline(config)
    AIP.run(steps)