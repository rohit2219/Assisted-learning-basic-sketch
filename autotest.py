#!/bb/bis2/Python-3.3.5/bin/python3
#rcharantharty
__author__ = 'rcharanthary'

from utils.common.extlenvexec import extlenvexec
from utils.classes.input import input_handle
from utils.common.get_product_prop import get_product_prop
from utils.classes.product_to_do import product_actions
from utils.classes.analyse_logs import analyse_logs
import logging
logger=logging.getLogger("main")
import datetime
import sys
import os
logging.basicConfig(level=logging.DEBUG)
input_handler=input_handle()
list_parms=input_handler.accept_args(sys.argv)
temp_final_opfile="/bb/bis/tmp/rohit/finalop.ksh"
product_name=list_parms[1]
sandbox_name=list_parms[2]
pricedate=list_parms[3]
prevdate=list_parms[4]


get_product_prop_handler=get_product_prop(product_name)
prod_properties=get_product_prop_handler.ret_prop(product_name)
print(prod_properties)

product_action_handler=product_actions(prod_properties,sandbox_name,pricedate)
####ret_msg=product_action_handler.reset_data()

analyse_logs_handler=analyse_logs(prod_properties,sandbox_name,pricedate)
log_in_erro_list=analyse_logs_handler.get_defective_lognames()
print(log_in_erro_list)
for logname in log_in_erro_list:
    possible_error_list=[]
    possible_error_list=analyse_logs_handler.analyse_log_file(logname)
    logger.debug("LOGNAME: " + logname)
    print("possible_error_list: " , possible_error_list)
    
    if len(possible_error_list) > 1 : 
        most_probable_err=analyse_logs_handler.fix_logs_error(possible_error_list)

        try:
            nowtime=datetime.datetime.now()
            temp_final_opfile_newname=temp_final_opfile+nowtime.isoformat()
            print("renaming",temp_final_opfile,temp_final_opfile_newname)
            os.rename(temp_final_opfile,temp_final_opfile_newname)
        except FileNotFoundError:
            pass

        fh_op=open(temp_final_opfile,"a")
        writeline="#!/bin/ksh " + "\n"
        fh_op.write(writeline)
        writeline="#####issues with " + logname + "\n"
        fh_op.write(writeline)
        if len(most_probable_err) <= 1 : 
            logger.debug("no errors found in most probable search" )

        for i_err in most_probable_err:
            if most_probable_err[i_err] == "file_sync":

                writeline= "rsync -azv " + i_err + " " + os.path.dirname(i_err.replace("/ixp",sandbox_name)) + "/" + "\n"
                fh_op.write(writeline)
                writeline= "rsync -azv " + i_err + " " + os.path.dirname(i_err.replace("/ixp","/bb/bis/deploy/onetime")) + "/" + "\n"
                fh_op.write(writeline)

            if most_probable_err[i_err] == "dir_sync":

                writeline= "rsync -azv " + i_err + "/*" + " " + os.path.dirname(i_err.replace("/ixp",sandbox_name)) + "/" + "\n"
                fh_op.write(writeline)
                writeline= "rsync -azv " + i_err + "/*"+ " " + os.path.dirname(i_err.replace("/ixp","/bb/bis/deploy/onetime")) + "/" + "\n"
                fh_op.write(writeline)

        fh_op.close()
        try:
            os.chmod(temp_final_opfile,mode=0o755)
        except OSError:
            pass

    else:
        logger.debug("no errors found in hig level search " + logname)
        
exit

#possible_error_list=['/ixpb/indexprod5/asiapac/production/apind_ap.MIP', '/ixpb/indexprod5/asiapac/production/ap_updt.rep', '/ixpb/indexprod5/asiapac/production/ap_extr.rep', '/ixpb/indexprod5/asiapac/production/apindex.q', '/ixpb/indexprod5/asiapac/bin/ap_template_isin.ok', '/ixpb/indexprod5/asiapac/bin/sb_ap.map', '/ixpb/indexprod5/asiapac/bin/apmpflat.map', '$QUERY', 'required', '/ixpb/indexprod/bin/process_ap.csh', 'apindex.q', '/ixpb/indexprod5/asiapac/production/apind_ap.MIP', 'required', '/ixpb/indexprod5/asiapac/production', '/ixpb/indexprod5/asiapac/bin', '/ixpb/indexprod/bin/process_ap.csh', 'apindex.q', '/ixpb/indexprod5/asiapac/production/apind_ap.MIP', 'required', '/ixpb/indexprod5/asiapac/production', '/ixpb/indexprod5/asiapac/bin']



exit()

