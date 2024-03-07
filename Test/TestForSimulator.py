import node.simulator as simulator_class
import copy
def TestForSimulator():
    gpu_num = 64
    offline_jobs = simulator_class.offline_job_generator(2000)
    online_jobs = simulator_class.online_job_generator(64)
    

    # for i in simulator_class.throught_list.keys():
    #     for j in simulator_class.throught_list[i]:
    #         print(j)

    test = simulator_class.simulator(GPU_num=gpu_num, algorithm='miso', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))
    test = simulator_class.simulator(GPU_num=gpu_num, algorithm='me', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))


def TestForFunction():
    pass
