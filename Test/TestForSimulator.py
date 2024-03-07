import node.simulator as simulator_class
import copy
def TestForSimulator():
    gpu_num = 32
    offline_jobs = simulator_class.offline_job_generator(500)
    online_jobs = simulator_class.online_job_generator(32)

    test = simulator_class.simulator(GPU_num=32, algorithm='miso', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))
    test = simulator_class.simulator(GPU_num=32, algorithm='me', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))


def TestForFunction():
    pass
