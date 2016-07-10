"""
    clang interface
"""

import datetime
import subprocess
import logging
import os.path as opath
import glob
import plistlib
import interface

#заменить всё на темповые файлы и директории

class Clang(interface.Interface):
    """
        interface for use clang
    """

    def __init__(self, conf):
        """
            init of clang py interface
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
        cur = glob.glob("{}/*.plist".format(path))
        res = []
        for i in cur:
            with open(i, "rb") as plistfile:
                obj = plistlib.load(plistfile)
                if obj["diagnostics"]:
                    res.append(obj)
        return res

    @staticmethod
    def __get_dir_name__():
        timevar = datetime.datetime.now()
        dirname = timevar.strftime("%d%m%Y_%H%M%S")
        dirname = opath.abspath("./{}".format(dirname))
        return dirname

    def get_res(self, path):
        """
            return result of analysis code from 'path'
        """
        interface.Interface.get_res(self, path)
        conf = self.get_conf()
        # формирование комманды
        cmd = [self.command, ]
        if "flags" in conf:
            cmd += self.get_conf()["flags"].split(',')
        for i in conf:
            if i not in ["flags", "makecommand", "configcommand"]:
                if len(i) == 1:
                    cmd.append("-{}".format(i))
                    cmd.append(conf[i])
                else:
                    cmd.append("--{}".format(i))
                    cmd.append(conf[i])
        cmd.append("-plist")
        cmd.append("-o")
        cmd.append(Clang.__get_dir_name__())
        if "configcommand" in conf:
            confcmd = cmd.copy()
            confcmd.append(conf["configcommand"])
            cmd_str = ""
            for i in confcmd:
                cmd_str += i
                cmd_str += " "
            outfile = open("outc_clang", "w+")
            errfile = open("errc_clang", "w+")
            self.logger.debug("scan-build config command: " + cmd_str)
            proc = subprocess.Popen(confcmd, cwd=path, stdout=outfile, stderr=errfile)
            proc.wait()
            retcode = proc.returncode
            for i in outfile:
                self.logger.info(i)
            for i in errfile:
                self.logger.error(i)
            self.logger.info("config return code is %d", retcode)
            outfile.close()
            errfile.close()
        if "makecommand" in conf:
            cmd.append(conf["makecommand"])
        else:
            cmd.append("make")
        # формирование строкового эквивалента комманды
        cmd_str = ""
        for i in cmd:
            cmd_str += i
            cmd_str += " "
        self.logger.debug("scan-build command: " + cmd_str)
        # запуск процесса
        proc = subprocess.Popen(cmd, cwd=path)
        proc.wait()
        outfile = open("out_clang", "w+")
        errfile = open("err_clang", "w+")
        self.logger.debug("scan-build config command: " + cmd_str)
        proc = subprocess.Popen(confcmd, cwd=path, stdout=outfile, stderr=errfile)
        proc.wait()
        retcode = proc.returncode
        for i in outfile:
            self.logger.info(i)
        for i in errfile:
            self.logger.error(i)
        self.logger.info("return code is %d", retcode)
        outfile.close()
        errfile.close()
        #buf_str = ""
        # запись вывода в log
        retcode = proc.returncode
        self.logger.info("return code is %d", retcode)
        err_arr = Clang.__load_report__(dirname)
        print(err_arr)
