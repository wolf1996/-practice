"""
    cppcheck interface
"""

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

    def get_res(self, path):
        """
            return result of analysis code from 'path'
        """
        interface.Interface.get_res(self, path)
        conf = self.get_conf()
        # формирование комманды
        cmd = [self.command, ]
        cmd += self.get_conf()["flags"].split(',')
        for i in conf:
            if i != "flags":
                cmd.append(i + '=' + conf[i])
        cmd.append("--xml-version=2")
        cmd.append(path)
        # формирование строкового эквивалента комманды
        cmd_str = ""
        for i in cmd:
            cmd_str += i
            cmd_str += " "
        self.logger.debug("cppcheck command: " + cmd_str)
        result = open("res", "w+")
        # запуск процесса
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=result)
        proc.wait()
        buf_str = ""
        # запись вывода в log
        retcode = proc.returncode
        if retcode:
            for j in proc.stdout.read():
                i = chr(j)
                if i == "\n":
                    self.logger.error(buf_str)
                    print(buf_str)
                    buf_str = ""
                else:
                    buf_str += i
            raise exceptions.ExecError("cppcheck error ")
        for j in proc.stdout.read():
            i = chr(j)
            if i == "\n":
                self.logger.info(buf_str)
                print(buf_str)
                buf_str = ""
            else:
                buf_str += i
        self.logger.info("return code is %d", retcode)
        result.close()
        xml = xmlt.parse("res")
        errors = xml.iter("error")
        err_arr = []
        for i in errors:
            err = {}
            err.update(i.attrib)
            loc = {}
            j = i.find("location")
            loc.update(j.attrib)
            err.update({"location": loc})
            err_arr.append(err)
        print(err_arr)
