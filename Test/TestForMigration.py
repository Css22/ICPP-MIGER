from util.sharing import *
from node.GPU_worker import woker
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as Scheduler_worker
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
from node.GPU_worker import *
import random


def test_migration():
    node1 = woker()
    node1.cluster_algorithm = 'me'
    test_job1 = online_job(model_name='resnet50', batch_Size=32, qos=45)
    test_job2 = offline_job(model_name='GAN', batch_Size=32, epoch=5)

    jobs1 = []
    jobs1.append(test_job1)
    test_job1.gi_id = 1
    jobs1.append(test_job2)
    # node1.GPU_list = [[test_job1,test_job2]]

    node1.GPU_list = [[[test_job1, test_job2]]]
    node1.config_list = [['1c-3g-40gb']]
    # MIG_operator.create_ins(0,'1c-3g-40gb' )
    node1.creation(0)

    time.sleep(30)
    node1.termination(0)
    node1.migrate_creation(0, )


    # print(node1.partition_optimizer(jobs=jobs1, GPU_index=0))
    # print(node1.GPU_list)
    # print(node1.config_list)