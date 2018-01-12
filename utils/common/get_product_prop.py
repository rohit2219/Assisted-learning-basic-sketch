__author__ = 'rcharanthary'
import sys
#sys.path.append('DIRPATH2/Python-3.3.5/packages/')
import logging
from utils.common.fileops import fileops
from utils.common.functions import print_class

class get_product_prop(object):
    def __init__(self,productname):
        self.return_prop={}
        self.prod_configfile="/home/rcharanthary/bin/autotest/convert-daily.txt"
        self.prin=print_class()
        self.logger=logging.getLogger("get_product_prop")
    def ret_prop(self,productname):
        return_prop=self.return_prop
        try :
            conf_file_obj=open(self.prod_configfile,"r")
            conf_file_handle=fileops(conf_file_obj)
            header_conf_file=conf_file_handle.file_read_line().strip().split("|")
        except:
            self.logger.error("check config file")
            conf_file_handle.file_close()
            raise

        for line in conf_file_obj:
            if line[0:1] == "#" or  line[0:1] == " ":
                break
            else:

                list_line=line.strip().split("|")
                if list_line[0] == productname:
                    return_prop=dict(zip(header_conf_file,list_line))

        if return_prop == {}:
            logging.error("check config file -2 ")
            conf_file_handle.file_close()
            raise

        conf_file_handle.file_close()

        return return_prop
