__author__ = 'rcharanthary'
import sys
sys.path.append('/bb/bis2/Python-3.3.5/site-packages/')
#{'productname': 'ASIAPAC', 'prod_backup_dir': 'indexprod5/asiapac/production/YYYYMMDD', 'prod_restart_scriptname': 'indexprod5/asiapac/bin/ASIAPAC-Restart-Script', 'prod_changes': 'indexprod5/asiapac/changes', 'prod_scriptname': 'indexprod5/asiapac/bin/ASIAPAC-Production-Script', 'prod_sunbond_dir': 'indexprod5/asiapac/datadir/daily', 'konsole_dir': 'indexprod5/asiapac/production/KONSOLE', 'automation_script': '/home/rcharanthary/gitbox/nightly_scripts/ASIAPAC_run.ksh /ixph YYYYMMDD', 'productdirectory': 'indexprod5/asiapac', 'prod_flags': 'indexprod5/asiapac/flags', 'prod_prices': 'indexprod5/asiapac/prices'}
import logging
import psutil
from utils.common.fileops import fileops
from utils.common.functions import print_class
from utils.common.functions import stringmatch_score
from utils.common.extlenvexec  import extlenvexec
from extnerr import *
import shutil
import os
import re
from multiprocessing import Queue

class analyse_logs(object):
    def __init__(self,prod_prop_dict,sandbox,pricedate):
        self.prod_prop_dict=prod_prop_dict
        self.sandbox=sandbox
        self.pricedate=pricedate
        self.return_code=0
        self.logger=logging.getLogger("analyse_logs")
        self.prin=print_class()
        self.acceptable_score=40
        self.backupdir="/bb/bis/bisdbfiles/"+pricedate+"_daily_new"
        prevdate="20170925"
        self.prevbackupdir="/bb/bis/bisdbfiles/"+prevdate+"_daily_new"
        self.rsync_cmd="rsync -azv "
        self.run_shellscript=extlenvexec()
        self.daily_dir=prod_prop_dict["prod_sunbond_dir"]
        self.prices_dir=prod_prop_dict["prod_prices"]
        self.change_dir=prod_prop_dict["prod_changes"]
        self.productdirectory=prod_prop_dict["productdirectory"]
        self.flags_dir=prod_prop_dict["prod_flags"]
        self.prod_back_dir=prod_prop_dict["prod_backup_dir"].replace("YYYYMMDD",str(pricedate))
        self.temp_log="/bb/bis/tmp/automonitor.log"
        self.temp_log2="/bb/bis/tmp/automonitor2.log"
        self.save_changes=sandbox+"/"+self.change_dir+"/save-changes"
        self.tail_cnt='100'
        self.unix_error=["file does not exist","abort","Variable syntax","cannot open","can't open"]

        self.ext_note=filename_extn_err
        self.pattern_files=self.ext_note + [self.sandbox]
        self.error_search_range=10
        self.no_logs_to_analyse=2

    def search_pattern(self,pattern_dict,srch_line):
        ret_code=False
        combine_pattern="(" + ")|(".join(pattern_dict) + ")"
        #self.logger.debug("combine_pattern:"+combine_pattern)
        #self.logger.debug("srch_line:"+srch_line)
        try:
            search_string=re.search(combine_pattern, srch_line,re.IGNORECASE).group(0)
        except AttributeError:
            search_string=""
        if search_string != "":
            ret_code=True
        return ret_code

    def convert_q_to_list(self,q_obj):
        ret_list=[]
        while 1:
            try:
                if q_obj.empty() is True:
                    break
                else:
                    ret_list.append(q_obj.get_nowait())
            except queue.Full:
                q_obj.get_nowait()
            except q_obj.empty():
                continue
        print("returning")
        self.logger.debug(ret_list)
        return ret_list
## gets all the logsnames which could have the highest possiblity of ABORT
    def get_defective_lognames(self):
        list_logs=[]
        list_cmd="ls -1tr " +  self.sandbox + "/" + self.prod_back_dir + "/" + " | tail -" + str(self.no_logs_to_analyse)
        self.run_shellscript.run_shell_script_py30(list_cmd,self.temp_log,"yes","True")
        fh=open(self.temp_log,"r+")
        for logname in fh:
            list_logs.append(self.sandbox + "/" + self.prod_back_dir + "/" + logname)
        fh.close()
        try:
            os.remove(self.temp_log)
        except FileNotFoundError:
            pass


        list_cmd="ls -1tr " +  self.sandbox + "/" + self.prod_back_dir + "/KONSOLE*" + " | tail -1"
        self.run_shellscript.run_shell_script_py30(list_cmd,self.temp_log,"yes","True")
        fh=open(self.temp_log,"r+")
        for logname in fh:
            list_logs.append(logname)
        fh.close()
        return list_logs
###searches the logfile for patterns around unix aborts
    def analyse_log_file(self,logfile):
        ret_code="555"
        count_line=0
        error_line_cnt=0
        tail_dict=[]
        error_found=False
        list_err_files=[]
    ##tail the log
        tail_cmd="tail -" + self.tail_cnt + " " + logfile
        self.logger.debug(tail_cmd)
        self.logger.debug("logfile:"+logfile)

        try:
            os.remove(self.temp_log)
        except FileNotFoundError:
            pass

        self.run_shellscript.run_shell_script_py30(tail_cmd,self.temp_log,"yes","True")
        self.logger.debug("tail done")

        fh=open(self.temp_log,"r+")

        prevq=Queue(maxsize=self.error_search_range)
        nextq=Queue(maxsize=self.error_search_range)
        list_around_errmsg=[]
        self.logger.debug("queue assigned")
        for xx in fh:
            line=fh.readline()
            self.logger.debug("lineb4err:"+line)
            count_line=count_line+1
            try:
                if prevq.full() is True:
                    try:
                        x=prevq.get_nowait()
                    except prevq.empty():
                        pass
                prevq.put_nowait(line)
            except queue.full():
                prevq.get_nowait()
            except prevq.empty():
                pass

            if self.search_pattern(self.unix_error,line) is True:
                self.logger.debug("errorline:"+line)
                error_line_cnt=count_line
                range_err_line=range(error_line_cnt-self.error_search_range,error_line_cnt+self.error_search_range)
                error_found=True
                nextq.put_nowait(line)

                for i in range(self.error_search_range):
                    line=fh.readline()
                    print("line aft error:",line)
                    try:
                        if nextq.full() is True:
                            try:
                                nextq.get_nowait()
                            except queue.empty():
                                pass

                        nextq.put_nowait(line)
                    except queue.full():
                        nextq.get_nowait()
                    except queue.empty():
                        continue
            if error_found is True:
                    break
        fh.close()

        list_prevq=self.convert_q_to_list(prevq)
        self.logger.debug("prevq: done")
        list_nextq=self.convert_q_to_list(nextq)
        self.logger.debug("nextq done")

        list_around_errmsg=list_prevq+list_nextq

        ## Now comes the part of analysing error
        print("error around err",list_around_errmsg)
        print("self.pattern_files",self.pattern_files)
        for  sent in list_around_errmsg:
            for word in sent.split():
                if self.search_pattern(self.pattern_files,word) is True:
                    list_err_files.append(word)
        print("error dirs files",list_err_files)


        if error_line_cnt == 0:
            return list_err_files
        return list_err_files


    ## studies the error files , query files and rep files and checks if any of them ae missing,if yes, then take action
    def fix_logs_error(self,pass_list_err):
        temp_pass_list_err=pass_list_err
        pass_list_err=[]
        ## removing dups
        for i_pass in temp_pass_list_err:
            if i_pass not in pass_list_err:
                pass_list_err.append(i_pass)

        extn_to_be_noted=self.ext_note
        extn_noted_list=[]
        imp_extn=[self.sandbox]
        imp_list=[]
        master_sandbox='/ixp'
        master_production_dir=master_sandbox+ "/" + self.productdirectory + "/" + "production"
        final_err_list=[]
        err_for_sure_dict={'possiblemiss':'type'}
        for list_file in pass_list_err:
            if self.search_pattern(extn_to_be_noted,list_file) is True:
#                print("found:",list_file)
                extn_noted_list.append(list_file)
            if self.search_pattern(imp_extn,list_file) is True:
#                print("important",list_file)
                imp_list.append(list_file)

        print(extn_noted_list)
        print(imp_list)
        ### process the important extns first, check if file or directory exists
        for i_list in imp_list:
            const=""
            i_list_ixpname=i_list.replace(self.sandbox,master_sandbox)
            if (os.path.exists(i_list_ixpname) is True) and (os.path.exists(i_list) is False):
                if os.path.isdir(i_list_ixpname) is True:
                    const="dict_sync"
                else:
                    const="file_sync"

                err_for_sure_dict[i_list]=const

        for j_list in extn_noted_list:
            #find_cmd="find  /ixp/indexprod5/euroagg/production/ -name "*dontprc.except*""
            find_cmd="find " + master_production_dir + "/" + " -name " + "\"" + "*" + j_list + "*" + "\""
            print(find_cmd)
            try:
                os.remove(self.temp_log2)
            except FileNotFoundError:
                pass

            self.run_shellscript.run_shell_script_py30(find_cmd,self.temp_log2,"yes","True")
            fh_log=open(self.temp_log2,"r+")
            for loop_line in fh_log:
                temp_line=loop_line.strip()
                print ("find:",temp_line)
                temp_line_sandboxname=temp_line.replace(master_sandbox,self.sandbox)

#                print("ixp file ",temp_line,os.path.exists(temp_line))
#                print("ixpb file",temp_line_sandboxname,os.path.exists(temp_line_sandboxname))

                if ( os.path.exists(temp_line) is True) and ( os.path.exists(temp_line_sandboxname) is False):
                    if os.path.isdir(temp_line_sandboxname) is True:
                        err_for_sure_dict[temp_line]="dict_sync"
                    else:
                        err_for_sure_dict[temp_line]="file_sync"
            fh_log.close()
        print(err_for_sure_dict)

        return err_for_sure_dict
