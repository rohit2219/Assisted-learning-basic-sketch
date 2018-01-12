__author__ = 'charantr'
import sys
import os
import shutil
import  datetime
from datetime import datetime
import re
import difflib 
import logging

class stringmatch_score:
      def __init__(self):
          self.default=""
      def stringmatch_difflib(self,string_a,string_b):
          ##uses the ratfcliff/obershelp algorithm to return a percentage of match between two strings
          match_score=difflib.SequenceMatcher(None,string_a,string_b).ratio() * 100
          return match_score

class print_class:
    def __init__(self):
        self.print_var=""
        self.print_rest=""
    def print_errorprogram(self,errorpoint, error_instance):
        print ('!!!!!!!ERROR ERROR !!!!!')
        print ('!!!!!!!exiting program with error!!!!!')
        print ("The script has exited at error code:",errorpoint,"and function:",error_instance)
        print ('use the above variables to pinpoint the error location in code')
        sys.exit()
    def print_function(self,print_msg,*print_rest):
        print(print_val)
        if print_rest[0] > 0:
            print(print_rest)
        return 0
    def print_char(self,print_char):
        print(print_char)

#call shell script , execute it and return the return code
def call_shell_script(scriptname,logfilename):
    ret=0

    if (logfilename and scriptname):
        # commented out the logging part as we are facing difficuly with retocode check
        call_scriptname=scriptname
    else:
        print_class.print_errorprogram("provide a log file too in the call","")
        print_class.print_errorprogram( "1","call_shell_script")


    ret=os.WEXITSTATUS(os.system(call_scriptname))
    #   #runs shell  script and returns return code too
    print_class.print_function("return_code",ret)

    if (ret == 0):
        function_return_code=0
    else:
        function_return_code=1
    return function_return_code

#Finds a string in file in the first position, parses the file using a delimiter and returns the parsed line in a tuple (kinda array)

def filefind(file_name, find_string,find_delimiter):
    #    print file_name,find_string,find_delimiter
    try:
        fo=open(file_name, "r+")
    except IOError as e:
        print_val="I/O error({0}):"+ format(e.errno, e.strerror)
        print_function(print_val)
        tup_line_return="NULL"

    for line in fo:
        tup_line=line.split(find_delimiter)
        if ( tup_line[0] == find_string ):
            tup_line_return=tup_line
    try:
        fo.close()
    except IOError as e:
        print_val="I/O error({0}):"+ format(e.errno, e.strerror)
        print_function(print_val)
    return tup_line_return

# temorary function is supposed to read only max of 100 variables,intended mainly for small config files.

def fileread(read_file_name):
    try:
        fr=open(read_file_name, "r+")
    except IOError as e:
        print_val="I/O error({0}):"+ format(e.errno, e.strerror)
        print_function(print_val)
        #    print read_file_name
        tup_line_read="NULL"

        temp_var=fr.read()
        tup_line_read=temp_var.split("\n")
        if (len(tup_line_read) > 99):
            print_function("the function is supposed to read only max of 100 variables, for raeding bigger files, use better methods")
        tup_line_read="ERROR"


    try:
        fr.close()
    except IOError as e:
        print_val="I/O error({0}):"+ format(e.errno, e.strerror)
        print_function(print_val)
    return tup_line_read

#converting YYYYMMDD date format to julian date format

def juliandateconvert(pass_date):

    year=int(str(pass_date)[0:4])
    month=int(str(pass_date)[4:6])
    day=int(str(pass_date)[6:8])
    a=(14 - month)//12;y=year + 4800 - a;m=month + 12*a - 3
    juliandate=day + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - 32045
    return(juliandate)

#copying from from_dir to to_dir

def copy_dir(from_dir,to_dir):
    ret_code=0
    try:
        src_files = os.listdir(from_dir)
    except OSError:
        errorprogram( "2","copy_dir")
        ret_code=12
    print_val="copying all files of(no subdir)"+from_dir+"to"+to_dir
    print_function(print_val)
    last_copy_file=from_dir
    for file_name in src_files:

        full_file_name = os.path.join(from_dir,file_name)

    if not os.path.isdir(full_file_name):

        if os.path.isfile(full_file_name):
            try:
                shutil.copy(full_file_name, to_dir)
            except IOError:
                print_function("last copied file",last_copy_file)
                print_function("Unable to copy file.",full_file_name)
                print_class.errorprogram( "3a","copy_dir")
            last_copy_file=full_file_name
        else:
            print_function("error while copying",full_file_name)
            print_function("last copied file:",last_copy_file)
            print_class.errorprogram( "3b","copy_dir")
            ret_code=12

    return ret_code


# used in the function multiple_replace
def make_xlat(*args, **kwds):
    adict = dict(*args, **kwds)
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    def xlat(text):
        return rx.sub(one_xlat, text)
    return xlat
# this is a code which does multiple string substitutions 1) text is the string in which you need to do the substitution and adict is a dictionary which would contain the "source" and "dest" strings to be changed.
def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


