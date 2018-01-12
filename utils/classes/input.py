__author__ = 'charantr'
#  a generic input handling classes. Most of the inputs which we recieve here are numbers or files, this class validates both

from utils.common.functions import print_class
import os

class input_handle(object):
    def __init__(self):
        self.usermessage=""
        self.arg_l=""
        self.prin=print_class()
        usage="scriptname <productname sandbox>"

    def accept_args(self,getargs):
        list_args=getargs
        return  getargs
   
