from argparse import ArgumentParser
import yaml
from Download.downloader import Downloader

class AI_pipeline():
    def __init__(self,config):
        self._config = config

    def run(self,steps):
        for step in steps:
            print(self._config)
            self._downloader = Downloader(self._config[step.capitalize()])
            self._downloader.crowl()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("config", help="yaml config defining the training pipleline", type=str)
    parser.add_argument("--download", help="Run download module",action='store_false')
    args = parser.parse_args()

    config_file_path = getattr(args, 'config', False)

    with open(config_file_path,encoding='utf8') as f:
        config = yaml.safe_load(f)


    steps=[k for k,v in vars(args).items() if v==True] # get the --keys in arguments

    if not steps : # if the user is too stupid to give args we will get it for him
        steps=[k.lower() for k in config.keys()]

    AIP = AI_pipeline(config)
    AIP.run(steps)