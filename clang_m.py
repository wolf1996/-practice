"""
    clang interface
"""

import copy
import datetime
import subprocess
import logging
import os.path as opath
import glob
import plistlib
import interface

# заменить всё на темповые файлы и директории


class Clang(interface.Interface):
    """
        interface for use clang
    """

    @staticmethod
    def __normalize__(filename, elem):
        elem["message"] = elem["description"]
        del elem["description"]
        elem["location"]["file"] = opath.basename(filename)
        elem.update({"next result": []})
        return elem

    def __init__(self, conf):
        """
            build init of clang py interface
        """
        interface.Interface.__init__(self, conf)
        self.command = "scan-build"
        self.logger = logging.getLogger(__name__)
        self.logger.info("clang module inited")

    @staticmethod
    def __load_report__(path):
        """
            load from file some data in xml format and
            parse it
        """
        cur = glob.glob("{}/**/*.plist".format(path))
        res = []
        for i in cur:
            with open(i, "rb") as plistfile:
                obj = plistlib.load(plistfile)
                if obj["diagnostics"]:
                    res.append(obj)
        return res

    @staticmethod
    def __get_dir_name__():
        """
            get directory name
        """
        timevar = datetime.datetime.now()
        dirname = timevar.strftime("%d%m%Y_%H%M%S")
        dirname = opath.abspath("./{}".format(dirname))
        return dirname

# комманды добавляюще анализируемую комманду к команде анализатора
# из-за проблем с относительными путями

    def __clean_command(self, cmd, path):
        """
            clean command
        """
        conf = self.get_conf()
        if "cleancommand" in conf:
            cmd = copy.copy(cmd)
            com = conf["cleancommand"].split()
            bufcom = opath.join(path, com[0])
            if opath.isfile(bufcom):
                com[0] = bufcom
            cmd += com
            cmd_str = ""
            for i in cmd:
                cmd_str += i
                cmd_str += " "
            self.logger.debug("scan-build clean command: " + cmd_str)
            outfile = open("out_clean_clang", "w+")
            errfile = open("err_clean_clang", "w+")
            print(path)
            print(cmd)
            proc = subprocess.Popen(
                cmd, cwd=path, stdout=outfile, stderr=errfile)
            proc.wait()
            retcode = proc.returncode
            for i in outfile:
                self.logger.info(i)
            for i in errfile:
                self.logger.error(i)
            self.logger.info("clean return code is %d", retcode)
            outfile.close()
            errfile.close()

    def __config_command(self, cmd, path):
        """
            config command
        """
        conf = self.get_conf()
        if "configcommand" in conf:
            cmd = copy.copy(cmd)
            com = conf["configcommand"].split()
            bufcom = opath.join(path, com[0])
            if opath.isfile(bufcom):
                com[0] = bufcom
            cmd += com
            cmd_str = ""
            for i in cmd:
                cmd_str += i
                cmd_str += " "
            self.logger.debug("scan-build config command: " + cmd_str)
            outfile = open("out_conf_clang", "w+")
            errfile = open("err_conf_clang", "w+")
            print(path)
            print(cmd)
            proc = subprocess.Popen(
                cmd, cwd=path, stdout=outfile, stderr=errfile)
            proc.wait()
            retcode = proc.returncode
            for i in outfile:
                self.logger.info(i)
            for i in errfile:
                self.logger.error(i)
            self.logger.info("clean return code is %d", retcode)
            outfile.close()
            errfile.close()

    def __make_command(self, cmd, path):
        """
            make command
        """
        cmd = copy.copy(cmd)
        conf = self.get_conf()
        if "makecommand" in conf:
            com = conf["makecommand"].split()
            bufcom = opath.join(path, com[0])
            if opath.isfile(bufcom):
                com[0] = bufcom
            cmd += com
        else:
            cmd.append("make")
        cmd_str = ""
        for i in cmd:
            cmd_str += i
            cmd_str += " "
        self.logger.debug("scan-build make command: " + cmd_str)
        outfile = open("out_make_clang", "w+")
        errfile = open("err_make_clang", "w+")
        print(path)
        print(cmd)
        proc = subprocess.Popen(
            cmd, cwd=path, stdout=outfile, stderr=errfile)
        proc.wait()
        retcode = proc.returncode
        for i in outfile:
            self.logger.info(i)
        for i in errfile:
            self.logger.error(i)
        self.logger.info("clean return code is %d", retcode)
        outfile.close()
        errfile.close()

    def get_res(self, path):
        """
            return result of analysis code from 'path'
        """
        path = opath.abspath(path)
        interface.Interface.get_res(self, path)
        conf = self.get_conf()
        # формирование комманды (всё относящееся к анализатору)
        cmd = [self.command, ]
        if "flags" in conf:
            cmd += self.get_conf()["flags"].split(',')
        for i in conf:
            if i not in ["flags", "makecommand",
                         "configcommand", "cleancommand"]:
                if len(i) == 1:
                    cmd.append("-{}".format(i))
                    cmd.append(conf[i])
                else:
                    cmd.append("--{}".format(i))
                    cmd.append(conf[i])
        cmd.append("-plist-html")
        cmd.append("-o")
        # Clang.__get_dir_name__()
        dirname = Clang.__get_dir_name__()#"/home/ksg/disk_d/labs_2016/practic/ms/practice/14072016_005323/"
        cmd.append(dirname)
        self.__config_command(cmd, path)
        self.__make_command(cmd, path)
        self.__clean_command(cmd, path)
        #buf_str = ""
        # запись вывода в log
        pars = Clang.__load_report__(dirname)
        err_arr = []
        for i in pars:
            err_arr += i["diagnostics"]
        # print(err_arr)
        #return map(lambda x: Clang.__normalize__(
        #   pars[0]["files"][0], x), err_arr)
        res_arr = [Clang.__normalize__(pars[0]["files"][0], i) for i in err_arr]
        return res_arr
