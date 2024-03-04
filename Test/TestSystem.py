from util.sharing import *
from node.GPU_worker import woker
import node.GPU_worker as GPU_worker
import node.Scheduler_worker as Scheduler_worker
import util.MIG_operator as MIG_operator
import util.MPS_operator as MPS_operator
from node.GPU_worker import *
import random



def testForPartitionOptimizer():
    node1 = woker()
    node1.cluster_algorithm = 'me'

    online_job1 = online_job(model_name='resnet50', batch_Size=32, qos=100, jobid=0)
    online_job2 = online_job(model_name='resnet50', batch_Size=32, qos=100, jobid=1)

    offline_job1 =  offline_job(model_name='GAN', batch_Size=32, epoch=5, jobid=2)
    offline_job2 =  offline_job(model_name='GAN', batch_Size=32, epoch=5, jobid=3)


    jobs_list = []
    jobs_list.append(online_job1)
    jobs_list.append(online_job2)
    jobs_list.append(offline_job1)
    jobs_list.append(offline_job2)

    node1.partition_optimizer(jobs_list, GPU_index=0)

def testForAllocateAvaliable():
    node1 = woker()
    node1.cluster_algorithm = 'me'

    online_job1 = online_job(model_name='resnet50', batch_Size=32, qos=50, jobid=0)
    online_job2 = online_job(model_name='resnet50', batch_Size=32, qos=50, jobid=1)
    # online_job3 = online_job(model_name='resnet50', batch_Size=32, qos=100, jobid=2)
    offline_job1 =  offline_job(model_name='resnet50', batch_Size=32, epoch=5, jobid=3)

    jobs_list = []
    jobs_list.append(online_job1)
    node1.partition_optimizer(jobs_list, 0)
    simulate_execution(jobs_list)

    for i in jobs_list:
        print(i.jobid, i.gi_id , i.new_gi_id)

    jobs_list.append(online_job2)
    node1.partition_optimizer(jobs_list, 0)
    simulate_execution(jobs_list)

    # for i in jobs_list:
    #     print(i.jobid, i.gi_id , i.new_gi_id)
    # jobs_list.append(online_job3)
    # node1.partition_optimizer(jobs_list, 0)
    # simulate_execution(jobs_list)

    for i in jobs_list:
        print(i.jobid, i.gi_id , i.new_gi_id)

    jobs_list.append(offline_job1)
    node1.partition_optimizer(jobs_list, 0)
    simulate_execution(jobs_list)
    for i in jobs_list:
        print(i.jobid, i.gi_id , i.new_gi_id)


    # online_job1.gi_id = 7
    # # online_job1.gi_id = 5
    # # online_job2.gi_id = 4
    # # online_job3.gi_id = -1

    # # online_config = [2,2,3]
    # # item = [2,2,3]

    
    # # for i in jobs_list:
    # #     print(i.new_gi_id, i.gi_id)
    # # index = global_config_list.index(item)
    # # print(node1.allocate_avaliable(online_jobs=jobs_list, online_config=online_config, config=item))

    # # node1.config_list = [['1c-3g-40gb', '1c-2g-20gb', '1c-2g-20gb']]
    # # node1.GPU_list = [[[online_job3], [online_job2], [online_job1]]]
    # # print(node1.migrate_order(0))

    # # for i in jobs_list:
    # #     print(i.new_gi_id, i.gi_id)

    # node1.partition_optimizer(jobs_list, 0)


def test_running():
    node1 = woker()
    node1.cluster_algorithm = 'me'
    job_list = []
    online_job1 = online_job(model_name='resnet50', batch_Size=32, qos=50, jobid=0)
    online_job2 = online_job(model_name='resnet50', batch_Size=32, qos=50, jobid=1)
    offline_job1 =  offline_job(model_name='resnet50', batch_Size=32, epoch=5, jobid=3)

    job_list.append(online_job1)
    job_list.append(online_job2)
    job_list.append(offline_job1)

    for i in job_list:
        node1.node_schedule(gpu_id=0, new_job=i)
        time.sleep(30)

def simulate_execution(jobs):
    for i in jobs:
        i.gi_id = i.new_gi_id

