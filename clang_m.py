"""
    clang interface
"""
import argparse
import os.path
import sys
import interface
import subprocess as sub
import logging

class Clang(interface.Interface):
    """
        interface for use clang
    """
    def __init__(self, conf):
        """
            init of clang py interface
        """
        interface.Interface.__init__(self, conf)
        command = "clang"
        self.logger = logging.getLogger(__name__)
        self.logger.info("clang module inited")

    def get_res(self, path):
        """
            return result of analysis code from 'path'
        """
        interface.Interface.get_res(self, path)