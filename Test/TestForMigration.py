from util.sharing import *
from node.GPU_worker import woker
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as Scheduler_worker
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
from node.GPU_worker import *
import random


def test_function_migrate_creation():
    node1 = woker()
    node1.cluster_algorithm = 'me'

    GPU_worker.regist_worker()
    node1.start_update_load()
    restart_thread = threading.Thread(target=restart_dcgm)
    restart_thread.start()
    test_job1 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job2 = offline_job(model_name='GAN', batch_Size=32, epoch=5, jobid=1)

    jobs1 = []
    jobs1.append(test_job1)
    test_job1.gi_id = 2
    test_job2
    jobs1.append(test_job2)
    # node1.GPU_list = [[test_job1,test_job2]]

    node1.GPU_list = [[[test_job1]]]
    node1.config_list = [['1c-3g-40gb']]
    # MIG_operator.create_ins(0,'1c-3g-40gb' )
    node1.creation(0)

    time.sleep(30)
    # node1.termination(0)

    print("start migrating")
    # node1.migrate_creation(gpu_id=0, new_gi_id=1, config='1c-3g-40gb', online_job_item=test_job1, offline_job_item=test_job2)
    node1.migrate_creation(gpu_id=0, new_gi_id=1, config='1c-3g-40gb', online_job_item=test_job1)

    # print(node1.partition_optimizer(jobs=jobs1, GPU_index=0))
    # print(node1.GPU_list)
    # print(node1.config_list)


def test_function_migrate_order():
    node1 = woker()
    node1.cluster_algorithm = 'me'

    test_job1 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job2 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job3 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job4 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)

    test_job1.gi_id = 9
    test_job1.new_gi_id = 12

    test_job2.gi_id = 7
    test_job2.new_gi_id = 13

    test_job3.new_gi_id = 1
    test_job3.gi_id = -1

    test_job4.new_gi_id = 11
    test_job4.gi_id = 12
    node1.GPU_list = [[[test_job1], [test_job2], [test_job3], [test_job4]] ]
    print(node1.migrate_order(0))

def test_function_do_migrate():
    node1 = woker()
    node1.cluster_algorithm = 'me'

    test_job1 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job2 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job3 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)
    test_job4 = online_job(model_name='resnet50', batch_Size=32, qos=45, jobid=0)

    # test for success
    test_job1.jobid = 0
    test_job2.jobid = 1
    test_job3.jobid = 2
    test_job4.jobid = 3


    test_job1.gi_id = 9
    test_job1.new_gi_id = 11

    test_job2.gi_id = 7
    test_job2.new_gi_id = 13

    test_job3.gi_id = -1
    test_job3.new_gi_id = 1

    test_job4.gi_id = 8
    test_job4.new_gi_id = 12

    node1.GPU_list = [[[test_job1], [test_job2], [test_job4]]]
    node1.config_list = [['1c-1g-10gb', '1c-1g-10gb', '1c-1g-10gb']]

    # order_list = node1.migrate_order(0)
    # print(order_list)
    node1.creation(0) 
    node1.fix_job[0].append(test_job1)
    node1.fix_job[0].append(test_job2)
    node1.fix_job[0].append(test_job4)
    time.sleep(60)

    node1.GPU_list = [[[test_job1], [test_job2], [test_job3], [test_job4]] ]
    node1.config_list = [['1c-1g-10gb', '1c-1g-10gb','1c-4g-40gb','1c-1g-10gb']]

    node1.sorted(0)
    order_list = node1.migrate_order(0)
    print(order_list)
    if order_list:
        node1.do_migrate(gpu_id=0, order_list=order_list)   
        test_job3.gi_id = 1
        node1.creation(0)        
        print(node1.fix_job)                                   