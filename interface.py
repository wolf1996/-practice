"""
    base class to all modules
"""
import os.path
import logging
import exceptions


class Interface():
    """
        interface of classes
    """
    def __init__(self, conf):
        """
            init interface class
        """
        self.__conf = conf
        self.__path = None
        self.logger = logging.getLogger(__name__)

    def __set_path__(self, path):
        """
            set's path to analyzed code
        """
        if not os.path.exists(path):
            self.logger.error("wrong path %s", path)
            raise exceptions.ConfigFileError("Path is not exists")
        self.__path = path

    def get_res(self, path):
        """
            get result of analys
        """
        self.__set_path__(path)



    def get_code_path(self):
        """
            return path to code analysis
        """
        return self.__path

    def get_conf(self):
        """
            get configurations
        """
        return self.__conf

    def set_conf(self, conf):
        """
            configurations
        """
        self.__conf = conf


    @staticmethod
    def exist(path):
        """
            check path valid
        """
        if not os.path.exists(path):
            raise exceptions.ConfigFileError("Path is not exists")
        return path
