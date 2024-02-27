from util.sharing import *
from node.GPU_worker import woker
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as Scheduler_worker
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
from node.GPU_worker import *
import random


def TestForTree():
    used_list = [1,2]
    GI_ID = 13
    print(check_available(gi_id=GI_ID, used_list=used_list))


    used_list = [1,5]
    GI_ID = 13
    print(check_available(gi_id=GI_ID, used_list=used_list))