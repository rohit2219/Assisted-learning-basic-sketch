__author__ = 'charantr'
from utils.common.functions import print_class
import subprocess
import os

class extlenvexec():

    def __init__(self):
        self.file_name = ""
        self.print_class = print_class()
        self.fr = ""

#call shell script , execute it and return the return code, a new version of the process used in python 3 and above

    def run_shell_script_py30( self, scriptname, logfilename, printopt, shellopt ):

        ret_code = 0
        if shellopt == "True":
           pass
        elif shellopt == "False":
           pass
        else:
           self.print_class.print_char("Invalid Shellopt, valuid options are True and False")
           self.print_class.print_errorprogram( "16","run_shell_script")

        try:
            #print(scriptname, logfilename, printopt ,shellopt)
            log = open(logfilename,"w+")
            subprocess.call(scriptname,stdout=log,shell=shellopt)

            if printopt == "yes":
                for line in log:
                    print(line)
            log.close()

        except (IOError, subprocess.CalledProcessError):
            self.print_class.print_errorprogram( "16","run_shell_script")
            ret_code=99999
        return ret_code

#call shell script , execute it and return the return code,an old version of the process used in python 2.7 and below

    def run_shell_script_py27(self,scriptname,logfilename):

        if (logfilename and scriptname):
            call_scriptname=scriptname
        else:
            self.print_class.print_errorprogram("provide a log file too in the call","")
            self.print_class.print_errorprogram( "1","call_shell_script")

        ret=os.WEXITSTATUS(os.system(call_scriptname))
        self.print_class.print_function("return_code",ret)

        if (ret == 0):
            function_return_code=0
        else:
            function_return_code=1

        return function_return_code

