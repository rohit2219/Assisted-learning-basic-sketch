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

import sys
logging.basicConfig(level=logging.DEBUG)
input_handler=input_handle()
list_parms=input_handler.accept_args(sys.argv)

product_name=list_parms[1]
sandbox_name=list_parms[2]
pricedate=list_parms[3]
prevdate=list_parms[4]


get_product_prop_handler=get_product_prop(product_name)
prod_properties=get_product_prop_handler.ret_prop(product_name)
print(prod_properties)

product_action_handler=product_actions(prod_properties,sandbox_name,pricedate)
ret_msg=product_action_handler.reset_data()

#analyse_logs_handler=analyse_logs(prod_properties,sandbox_name,pricedate)
#possible_error_list=analyse_logs_handler.analyse_log_file("/ixpb/indexprod5/asiapac/production/20170926_old/process_ap_prepare.log-19394")
#possible_error_list=['/ixpb/indexprod5/asiapac/production/apind_ap.MIP', '/ixpb/indexprod5/asiapac/production/ap_updt.rep', '/ixpb/indexprod5/asiapac/production/ap_extr.rep', '/ixpb/indexprod5/asiapac/production/apindex.q', '/ixpb/indexprod5/asiapac/bin/ap_template_isin.ok', '/ixpb/indexprod5/asiapac/bin/sb_ap.map', '/ixpb/indexprod5/asiapac/bin/apmpflat.map', '$QUERY', 'required', '/ixpb/indexprod/bin/process_ap.csh', 'apindex.q', '/ixpb/indexprod5/asiapac/production/apind_ap.MIP', 'required', '/ixpb/indexprod5/asiapac/production', '/ixpb/indexprod5/asiapac/bin', '/ixpb/indexprod/bin/process_ap.csh', 'apindex.q', '/ixpb/indexprod5/asiapac/production/apind_ap.MIP', 'required', '/ixpb/indexprod5/asiapac/production', '/ixpb/indexprod5/asiapac/bin']

#analyse_logs_handler.fix_logs_error(possible_error_list)

exit()

