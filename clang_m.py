"""
    clang interface
"""
import subprocess
import logging
import interface

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
    def __load_file__(path):
        """
            load from file some data in xml format and
            parse it
        """
        return {}

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
        cmd.append("clangres")
        if "configcommand" in conf:
            confcmd = cmd.copy()
            confcmd.append(conf["configcommand"].replace("{PATH}", path))
            cmd_str = ""
            for i in confcmd:
                cmd_str += i
                cmd_str += " "
            self.logger.debug("scan-build config command: " + cmd_str)
            proc = subprocess.Popen(confcmd)
            proc.wait()
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
        proc = subprocess.Popen(cmd)
        proc.wait()
        #buf_str = ""
        # запись вывода в log
        retcode = proc.returncode
        self.logger.info("return code is %d", retcode)
        err_arr = []  # CppCheck.__load_file__("res")
        print(err_arr)
