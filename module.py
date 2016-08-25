"""
    application file
"""
import shutil
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

    @staticmethod
    def str_elem(elem):
        """
            return minimalistic notation of result
        """
        res_str = ""
        res_str += elem["type"] + "\n"
        res_str += "file :{file} line: {line} col: {col} \n".format(
            **(elem["location"]))
        res_str += elem["message"] + "\n"
        return res_str

    @staticmethod
    def __cmp_loc(rec1, rec2):
        loc1 = rec1["location"]
        loc2 = rec2["location"]
        res = 1
        res = (res and (loc1["file"] == loc2["file"]))
        res = (res and (loc1["line"] == loc2["line"]))
        res = (res and ((loc1["col"]) or (loc2["col"])))
        res = (
            res and (
                (not loc1["col"]) or (
                    not loc2["col"]) or (
                        loc1["col"] == loc2["col"])))
        return res

    @staticmethod
    def __merge(array):
        """
            merge array of results
        """
        merged_arr = []
        for j in array:
            if j in merged_arr:
                pos = merged_arr.index(j)
                merged_arr[pos]["next result"].append(j)
            else:
                merged_arr.append(j)
        return merged_arr

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
        # инициализация полей значениями по умолчанию
        self.logger = None
        self.__analyzers = []
        self.__workdir = '.'

    def get_res(self, path):
        """
            get result of analyse
        """
        curdir = os.getcwd()
        path = os.path.abspath(path)
        if self.__workdir != '.':
            if os.path.exists(self.__workdir):
                try:
                    shutil.rmtree(self.__workdir)
                except Exception:
                    raise exceptions.WorkDirError(
                        "can't remove {}".format(self.__workdir))
            try:
                os.mkdir(self.__workdir)
                os.chdir(self.__workdir)
            except Exception:
                raise exceptions.WorkDirError(
                    "can't create {}".format(self.__workdir))
        if self.logger:
            self.logger.info("scaning %s", path)
        if not os.path.exists(path):
            self.logger.error("code path '%s' is not exists", path)
            raise exceptions.ConfigFileError("Path is not exists")
        res_array = []
        # print("analyzers:")
        # print(self.__analyzers)
        for i in self.__analyzers:
            res = i.get_res(path)
            res_array += res
            print(i.get_report())
        res_array = App.__merge(res_array)
        try:
            os.chdir(curdir)
        except Exception:
            raise exceptions.WorkDirError("can't create {}".format(curdir))
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
        # print(self.__analyzers)

    def save_config_to_file(self, path):
        """
            save configuration to file
        """
        self.logger.info("save configuration to %s", path)
        confile = open(path, 'w')
        self.__config.write(confile)
        confile.close()

    def set_workdir(self, workdir):
        self.__workdir = os.path.abspath(workdir)
        self.logger.info("Working directory was changed to{}".format(workdir))

def get_workdir(self):
        return self.__workdir


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
    app_instance.set_workdir("./somedir/")
    res = app_instance.get_res(parsed.path)
    for i in res:
        # if "path" in i.keys():
        #    del i["path"]
        # print(i)
        buf = App.str_elem(i)
        print(buf)
        print("#######################################")


if __name__ == '__main__':
    main()
