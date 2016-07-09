"""
    cppcheck interface
"""

import re
import subprocess
import logging
import xml.etree.ElementTree as xmlt
import exceptions
import interface



class CppCheck(interface.Interface):
    """
        interface for use clang
    """

    def __init__(self, conf):
        """
            init of clang py interface
        """
        interface.Interface.__init__(self, conf)
        self.command = "cppcheck"
        self.logger = logging.getLogger(__name__)
        self.logger.info("cppcheck module inited")

    @staticmethod
    def __load_file__(path):
        """
            load from file some data in xml format and
            parse it
        """
        xml = xmlt.parse(path)
        errors = xml.iter("error")
        err_arr = []
        for i in errors:
            err = {}
            err.update(i.attrib)
            loc = {}
            if i:
                j = i.find("location")
            loc.update(j.attrib)
            err.update({"location": loc})
            err_arr.append(err)
        return err_arr

    def get_res(self, path):
        """
            return result of analysis code from 'path'
        """
        interface.Interface.get_res(self, path)
        conf = self.get_conf()
        # формирование комманды
        cmd = [self.command, ]
        if "flags" in conf:
            cmd += re.split(", | ", self.get_conf()["flags"])
        for i in conf:
            if i != "flags":
                cmd.append("--{0}={1}".format(i, conf[i]))
        cmd.append("--xml-version=2")
        cmd.append(path)
        # формирование строкового эквивалента комманды
        cmd_str = ""
        for i in cmd:
            cmd_str += i
            cmd_str += " "
        self.logger.debug("cppcheck command: " + cmd_str)
        result = open("res", "w+")
        output = open("out", "w+")
        # запуск процесса
        proc = subprocess.Popen(cmd, stdout=output, stderr=result)
        proc.wait()
        buf_str = ""
        # запись вывода в log
        retcode = proc.returncode
        if retcode:
            for j in output.read():
                i = chr(j)
                if i == "\n":
                    self.logger.error(buf_str)
                    print(buf_str)
                    buf_str = ""
                else:
                    buf_str += i
            raise exceptions.ExecError("cppcheck error ")
        for j in output.read():
            i = chr(j)
            if i == "\n":
                self.logger.info(buf_str)
                print(buf_str)
                buf_str = ""
            else:
                buf_str += i
        self.logger.info("return code is %d", retcode)
        result.close()
        err_arr = CppCheck.__load_file__("res")
        return err_arr
