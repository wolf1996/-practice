"""
    application file
"""
import configparser
import argparse
import os.path
import logging
import logging.config
import fabric
import exceptions


def exist(path):
    """
        check path valid
    """
    if not os.path.exists(path):
        msg = "type error"
        raise argparse.ArgumentTypeError(msg)
    return path


class App:
    """
        application class
    """

    def __init__(self):
        """
            initialisation of application class
        """
        # перепилить, выкинуть загрузку из конструктора, добавить дефолтную
        # конфигурацию
        config = configparser.ConfigParser()
        config.read_dict({
            'app': {'logfile': './log.txt',
                   },
        })
        self.__config = config
        self.__def_config = config
        self.__my_conf = self.__config["app"]
        self.__my_def_conf = self.__def_config["app"]
        #инициализация полей значениями по умолчанию
        self.logger = None
        self.__analyzers = []

    def get_res(self, path):
        """
            get result of analyse
        """
        if self.logger:
            self.logger.info("scaning %s", path)
        if not os.path.exists(path):
            self.logger.error("code path '%s' is not exists", path)
            raise exceptions.ConfigFileError("Path is not exists")
        res_array = []
        #print("analyzers:")
        #print(self.__analyzers)
        for i in self.__analyzers:
            res_array.append(i.get_res(path))
        return res_array

    def load_config_from_file(self, path):
        """
            load configuration from file
        """
        # соответствующие записи и проверка пути
        if self.logger:
            self.logger.info("loading configuration file %s", path)
        if not os.path.exists(path):
            if self.logger:
                self.logger.error("config file %s does'not exists", path)
            raise exceptions.ConfigFileError(
                "path {} is not exists".format(path))
        # загрузка конфигураций
        self.__config = configparser.ConfigParser()
        self.__config.read(path)
        # проверка наличия секции приложения (возможно можно выкинуть)
        if "app" not in self.__config:
            self.logger.error("can't find 'app' section in %s", path)
            raise exceptions.ConfigFileError(
                "There are no 'app' section in config file")
        self.__my_conf = self.__config["app"]
        # настройка логгирования
        logging.basicConfig(
            filename=self.__my_conf.get(
                "logfile",
                fallback=self.__my_def_conf["logfile"]),
            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.info("loaded configuration file %s", path)
        # генерируем интерфейсы анализаторов
        self.__analyzers = []
        for i in self.__config.sections():
            if i != "app":
                self.__analyzers.append(
                    fabric.Fabric.get_class_instance(i)(
                        self.__config[i]))
        #print(self.__analyzers)

    def save_config_to_file(self, path):
        """
            save configuration to file
        """
        self.logger.info("save configuration to %s", path)
        confile = open(path, 'w')
        self.__config.write(confile)
        confile.close()


def main():
    """
        main function to console work
    """
    parser = argparse.ArgumentParser(description="Some description")
    #parser.add_argument("path", type=exist)
    parser.add_argument("path")
    parsed = parser.parse_args()
    app_instance = App()
    app_instance.load_config_from_file("test.cfg")
    app_instance.get_res(parsed.path)


if __name__ == '__main__':
    main()
