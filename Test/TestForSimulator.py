import node.simulator as simulator_class
import copy
def TestForSimulator():
    gpu_num = 1000
    offline_jobs = simulator_class.offline_job_generator(10000)
    online_jobs = simulator_class.online_job_generator(2000)
    

    # for i in simulator_class.throught_list.keys():
    #     for j in simulator_class.throught_list[i]:
    #         print(j)

    test = simulator_class.simulator(GPU_num=gpu_num, algorithm='me', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))
    result_list = [x // 3600 for x in test]
    print(test)

    # test = simulator_class.simulator(GPU_num=gpu_num, algorithm='me', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))


def TestForFunction():
    pass
