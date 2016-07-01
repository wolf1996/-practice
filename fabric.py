"""
    fabric of interfaces of analizers
"""
import clang_m
import cppcheck_m
import exceptions


class Fabric(object):
    """
        fabric class
    """
    classes = {'clang': clang_m.Clang, 'cppcheck': cppcheck_m.CppCheck}
    def __init__(self):
        """
            init function
        """
    @staticmethod
    def get_class_instance(classname):
        """
            return class constructor function
        """
        if not classname in Fabric.classes.keys():
            raise exceptions.WrongAnalizerNameError("Wrong Analizer Name: {}".format(classname))
        return Fabric.classes[classname]
