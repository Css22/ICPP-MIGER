from util.sharing import *
from node.GPU_worker import woker
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as Scheduler_worker
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
from node.GPU_worker import *
import random



def test_job_metrices():
    handle_job_log()