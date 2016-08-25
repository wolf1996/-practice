class MyError(Exception):
    """
        My base exception to module
    """
    pass

class ConfigFileError(MyError):
    """
        error raise when config file have some error
    """
    def __init__(self, msg):
        """
            init error class
        """
        self.message = msg

class PathExistenceError(MyError):
    """
        error raise when file not existed
    """
    def __init__(self, msg):
        """
            init error class
        """
        self.message = msg

class WrongPathError(MyError):
    """
        error of wrong path error 
    """
    def __init__(self, msg):
        """
            init error class
        """
        self.message = msg

class WrongAnalizerNameError(MyError):
    """
        error of wrong analizer in conf file
    """
    def __init__(self, msg):
        """
            init error class
        """
        self.message = msg

class ExecError(MyError):
    """
        error of programm execution
    """
    def __init__(self, msg):
        """
            init error class
        """
        self.message = msg



class WorkDirError(MyError):
    """
        error of programm execution
    """
    def __init__(self, msg):
        """
            init error class
        """
        self.message = msg