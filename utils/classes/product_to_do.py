__author__ = 'rcharanthary'
import sys
import logging
import psutil
from utils.common.fileops import fileops
from utils.common.functions import print_class
from utils.common.functions import stringmatch_score
from utils.common.extlenvexec  import extlenvexec
import os
import glob

class product_actions(object):
    def __init__(self,prod_prop_dict,sandbox,pricedate):
        self.prod_prop_dict=prod_prop_dict
        self.sandbox=sandbox
        self.pricedate=pricedate
        self.return_code=0
        self.logger=logging.getLogger("reset_product class")
        self.prin=print_class()
        self.acceptable_score=40
        self.backupdir="DIRPATH/bisdbfiles/"+pricedate+"_daily_new"
        prevdate="20170925"
        self.prevbackupdir="DIRPATH/bisdbfiles/"+prevdate+"_daily_new"
        self.rsync_cmd="rsync -azv "
        self.run_shellscript=extlenvexec()
        self.daily_dir=prod_prop_dict["prod_sunbond_dir"]
        self.prices_dir=prod_prop_dict["prod_prices"]
        self.change_dir=prod_prop_dict["prod_changes"]
        self.flags_dir=prod_prop_dict["prod_flags"]
        self.prod_scriptname=prod_prop_dict["prod_scriptname"]
        self.prod_back_dir=prod_prop_dict["prod_backup_dir"].replace("YYYYMMDD",str(pricedate))
        self.logfile="DIRPATH/tmp/automonitor.log"
        self.save_changes=sandbox+"/"+self.change_dir+"/save-changes"

    def check_prod_running(self):
        ret_run=False
        stringmatch=stringmatch_score()
        product_scriptname=self.prod_prop_dict['prod_scriptname']
        self.logger.debug("checking if "+product_scriptname+" running for product ")

        for run_pid in psutil.pids():
            try :
                script_running=psutil.Process(run_pid).name()
            except NoSuchProcess:
                continue
            #self.logger.debug(script_running + " --comp--t " + product_scriptname)
            if stringmatch.stringmatch_difflib(script_running,product_scriptname) > self.acceptable_score:
                self.logger.debug("matched for"+script_running+product_scriptname)
                ret_run=True
        return ret_run

    def sync_from_backup_to_sandbox(self,from_dir,to_dir,daytosync):
        if daytosync=="prevday":
            from_back_dir=self.prevbackupdir
        else:
            from_back_dir=self.backupdir

        rsync_full_cmd=self.rsync_cmd + from_back_dir + "/" + from_dir  + " " + self.sandbox + "/" + to_dir
        self.logger.debug(rsync_full_cmd)
        self.run_shellscript.run_shell_script_py30(rsync_full_cmd,self.logfile,"no","True")

        return
    def sync_fromdir_todir(self,from_dir,to_dir):
        rsync_full_cmd=self.rsync_cmd + from_dir + "/*" + " " +  to_dir + "/"
        self.logger.debug(rsync_full_cmd)
        self.run_shellscript.run_shell_script_py30(rsync_full_cmd,self.logfile,"no","True")

        return

    def reset_data(self):
        self.logger.debug("resetting data")
        ret_msg=""
        print(self.check_prod_running())
        if self.check_prod_running() is False:
           #1) sync daily
               self.sync_from_backup_to_sandbox(self.daily_dir+"/*",self.daily_dir+"/","prevday")
               #2)  sync prices
               self.sync_from_backup_to_sandbox(self.prices_dir+"/*",self.prices_dir+"/","curday")
               #3)  sync changes
               self.sync_fromdir_todir(self.save_changes ,self.sandbox+"/"+self.change_dir )
               #4 remove flags

               self.logger.debug("clearing flags:"+self.sandbox+"/"+self.flags_dir)
               clear_dir=self.sandbox+"/"+self.flags_dir+"/*"
               for del_file in glob.glob(clear_dir):
                   try:
                       os.remove(del_file)
                   except OSError:
                       pass
               #5 chmod the prod script
               script_chmod=self.sandbox+"/"+self.prod_scriptname
               self.logger.debug("chmod 755 prodn script:"+script_chmod)
               try:
                  os.chmod(script_chmod,mode=0o755)
               except OSError:
                  pass
               #6 copy the *pricedate* files alone for esm.
               self.sync_from_backup_to_sandbox(self.change_dir +"/esm/*"+ self.pricedate + "*"  , self.change_dir + "/esm/","curday")

        else:
               ret_msg="productrunning"

        return ret_msg

