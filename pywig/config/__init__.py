import configparser
import pathlib


class Config:
    def __init__(self, env: str):
        self.env = env
        self.config = configparser.ConfigParser()

    def read_config(self):
        self.config.read(pathlib.Path(__file__).parent.resolve() / ('%s.conf' % self.env))
        return self.config
