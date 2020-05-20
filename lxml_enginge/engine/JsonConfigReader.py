from bin.lxml_enginge.interfaces.ConfigReader import ConfigReader

from interface import implements
import os
import json


class JsonConfigReader(implements(ConfigReader)):

    def __init__(self, json_file_path:str):
        if not os.path.exists(json_file_path):
            raise Exception("File {} not found".format(json_file_path))

        try:
            with open(json_file_path) as json_file:
                data = json.load(json_file)
                self.__data = data
        except Exception as ex:
            raise Exception("Unable to read json file {}, {}".format(json_file_path, ex))

    def read(self):
        return self.__data

