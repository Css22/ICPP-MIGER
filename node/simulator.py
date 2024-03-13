
import sys
import re
import glob
import random
import copy
# from schedule.scheduler.muxflow_scheduler import muxflow_sheduler
from jobs.profile.standardized_throughput import *
from util.sharing import *
from node.GPU_worker import *
import queue
random.seed(17)

job_list = get_job_list()
throught_list = get_throughput_double_list()


class simulator:
    def __init__(self, GPU_num, algorithm, online_jobs, offline_jobs, num=4, cluster_algorithm='number_of_job'):
        self.GPU_num = GPU_num
        self.algorithm = algorithm
        self.online_jobs = online_jobs
        self.offline_jobs = offline_jobs
        self.num = num
        self.queue_time = []
        self.JCT = []
        self.busy = []
        self.config_num = 0
        self.job_queue = queue.Queue()
        self.cluster_algorithm = cluster_algorithm

        self.simulate()

    def simulate(self):
    
        for i in range(0, self.GPU_num):
            self.busy.append(0)

        if self.algorithm == 'miso':
            node1 = woker()
            node1.cluster_algorithm = 'miso'
            
            node1.GPU_list = []
            node1.throughput = []
            node1.config_list = []
            node1.fix_job = []
            node1.SM_percentage = []
            for i in range(0, self.GPU_num):
                node1.GPU_list.append([])
                node1.throughput.append(0)
                node1.config_list.append([])
                node1.fix_job.append([])
                node1.SM_percentage.append([])


            for i in self.online_jobs:
                gpu_id = self.get_minworkload(node1)
                
                node1.simulator_schedule(i, gpu_id)
                self.simulate_executor(i)
            
            # for i in range(0, len(scheduler.GPU_list)):
            #     # I_set_gi_id(scheduler.GPU_list[i], scheduler.config_list[i])
            #     I_search_solution(scheduler.GPU_list[i], scheduler.config_list[i])


            for j in self.offline_jobs:
                gpu_id = self.get_minworkload(node1)
                if node1.simulator_schedule(j, gpu_id):
                    j.start_time = 0 
                    self.simulate_executor(i)
                else:

                    self.job_queue.put(j)

            # for i in  self.online_jobs:
            #     print(i.gi_id)

            for i in range(0, len(node1.GPU_list)):
                configs = node1.config_list[i]
                for j in range(0, len(node1.GPU_list[i])):
                    if len(node1.GPU_list[i][j]) == 1:
                        if isinstance(node1.GPU_list[i][j][0], online_job):
                            continue
                        if isinstance(node1.GPU_list[i][j][0], offline_job):
                            self.caculate_completion_time(node1.GPU_list[i][j][0], configs[j])
                    
       
            num = 0
            job_list = []


            while True:
                num = num + 1   
                for i in range(0, len(node1.GPU_list)):
                    remove_jobs = []
                    for j in range(0, len(node1.GPU_list[i])):
                        if len(node1.GPU_list[i][j]) == 1:
                            if isinstance(node1.GPU_list[i][j][0], offline_job):
                                node1.GPU_list[i][j][0].progress = node1.GPU_list[i][j][0].progress + node1.GPU_list[i][j][0].speed
                                if node1.GPU_list[i][j][0].progress>= node1.GPU_list[i][j][0].epoch:
                                    remove_jobs.append(node1.GPU_list[i][j][0])

                    if len(remove_jobs) != 0:
                        for z in remove_jobs:
                            z.end_time = num
                            job_list.append(z)
                            self.state_change(node1, i, z)

                        for j in range(0, len(node1.GPU_list)):
                            for z in range(0, len(node1.GPU_list[j])):

                                if len(node1.GPU_list[j][z]) == 1:
                                    if isinstance(node1.GPU_list[j][z][0], online_job):
                                        continue
                                    if isinstance(node1.GPU_list[j][z][0], offline_job):
                                        if node1.GPU_list[j][z][0].start_time == -1:
                                            node1.GPU_list[j][z][0].start_time = num
                      
                                        self.caculate_completion_time(node1.GPU_list[j][z][0], node1.config_list[j][z])
                                   

                if len(job_list) == self.num:
                    break
            self.caculate_system_metrics(jobs=job_list)

        if self.algorithm == 'me':


            node1 = woker()
            node1.cluster_algorithm = 'me'
            
            node1.GPU_list = []
            node1.throughput = []
            node1.config_list = []
            node1.fix_job = []
            node1.SM_percentage = []
            for i in range(0, self.GPU_num):
                node1.GPU_list.append([])
                node1.throughput.append(0)
                node1.config_list.append([])
                node1.fix_job.append([])
                node1.SM_percentage.append([])


            for i in self.online_jobs:
               
                gpu_id = self.get_minworkload(node1)
                node1.simulator_schedule(i, gpu_id)
                self.simulate_executor(i)
            

            # for i in range(0, len(scheduler.GPU_list)):
            #     # I_set_gi_id(scheduler.GPU_list[i], scheduler.config_list[i])
            #     I_search_solution(scheduler.GPU_list[i], scheduler.config_list[i])
            
            for j in self.offline_jobs:
               
                gpu_id = self.get_minworkload(node1)
                if node1.simulator_schedule(j, gpu_id):
                    j.start_time = 0 
                    self.simulate_executor(i)
                else:
                    self.job_queue.put(j)

                
            for i in range(0, len(node1.GPU_list)):
                configs = node1.config_list[i]
            
                for j in range(0, len(node1.GPU_list[i])):
                    if len(node1.GPU_list[i][j]) == 1:
                        if isinstance(node1.GPU_list[i][j][0], online_job):
                            continue
                        if isinstance(node1.GPU_list[i][j][0], offline_job):
                            self.caculate_completion_time(node1.GPU_list[i][j][0], configs[j])
                    
                    else:
                        if isinstance(node1.GPU_list[i][j][0], online_job):
                            find_optimal_SM
                            self.caculate_completion_time_concurrency(offline_job= node1.GPU_list[i][j][1], online_job= node1.GPU_list[i][j][0] ,config= configs[j], )
                        else:
                            self.caculate_completion_time_concurrency(offline_job= node1.GPU_list[i][j][0], online_job= node1.GPU_list[i][j][1] ,config= configs[j])
            
            

            num = 0
            job_list = []
          
            c = 0
            # for i in scheduler.GPU_list:
            #     print(i)
            # for i in scheduler.config_list:
            #     print(i)
            while True:
                num = num + 1
                print(num)
                for i in range(0, len(node1.GPU_list)):
                   
                    remove_jobs = []
                    for j in range(0, len(node1.GPU_list[i])):
                        if len(node1.GPU_list[i][j]) == 1:
                            if isinstance(node1.GPU_list[i][j][0], offline_job):
                                node1.GPU_list[i][j][0].progress = node1.GPU_list[i][j][0].progress + node1.GPU_list[i][j][0].speed
                                if node1.GPU_list[i][j][0].progress >= node1.GPU_list[i][j][0].epoch:
                                    remove_jobs.append(node1.GPU_list[i][j][0])
                            
                 
                        else:

                            if isinstance(node1.GPU_list[i][j][0], offline_job):
                                node1.GPU_list[i][j][0].progress = node1.GPU_list[i][j][0].progress + node1.GPU_list[i][j][0].speed
                                if node1.GPU_list[i][j][0].progress >= node1.GPU_list[i][j][0].epoch:
                                    remove_jobs.append(node1.GPU_list[i][j][0])
                                    c =  c + 1
                            
                            else:
                                node1.GPU_list[i][j][1].progress = node1.GPU_list[i][j][1].progress + node1.GPU_list[i][j][1].speed
                                if node1.GPU_list[i][j][1].progress >= node1.GPU_list[i][j][1].epoch:
                                    remove_jobs.append(node1.GPU_list[i][j][1])
                                    c =  c + 1
                    

                    if len(remove_jobs) != 0:
                        for z in remove_jobs:
                            
                         
                            z.end_time = num
                            job_list.append(z)
                            print(len(job_list), self.num)
                            self.state_change(node1, i, z)
                     
                       
                        for j in range(0, len(node1.GPU_list)):

                            for z in range(0, len(node1.GPU_list[j])):
                                if len(node1.GPU_list[j][z]) == 1:
                               
                                    if isinstance(node1.GPU_list[j][z][0], online_job):
                                        continue
                                    if isinstance(node1.GPU_list[j][z][0], offline_job):
                                        
                                        if  node1.GPU_list[j][z][0].start_time == -1:
                                            node1.GPU_list[j][z][0].start_time = num
                    
                                        self.caculate_completion_time(node1.GPU_list[j][z][0], node1.config_list[j][z])
                    
                                else:
                                  
                                    if isinstance(node1.GPU_list[j][z][0], online_job):
                                        if  node1.GPU_list[j][z][1].start_time == -1:
                                            node1.GPU_list[j][z][1].start_time = num
                                         
                                        self.caculate_completion_time_concurrency(node1.GPU_list[j][z][1], node1.GPU_list[j][z][0], node1.config_list[j][z])
                                    else:
                                        if  node1.GPU_list[j][z][0].start_time == -1:
                                            node1.GPU_list[j][z][0].start_time = num
                                        self.caculate_completion_time_concurrency(node1.GPU_list[j][z][0], node1.GPU_list[j][z][1], node1.config_list[j][z])
                if len(job_list) == self.num :
                    # for i in job_list:
                    #     print(i)
                    break
            self.caculate_system_metrics(jobs=job_list)
            
        # if self.algorithm == 'me_with_over_resource':
        #     GPU_list = []
        #     for i in range(0, self.GPU_num):
        #         GPU_list.append([])
            
        #     scheduler = I_sheduler_with_over_resource(GPU_list= GPU_list, cluster_algorithm=self.cluster_algorithm)
        #     for i in self.online_jobs:
        #         scheduler.I_cluster(i)

        #     for j in self.offline_jobs:
        #         if scheduler.I_cluster(j):
        #             j.start_time = 0 
          
            
        #     for i in range(0, len(scheduler.GPU_list)):
        #         configs = scheduler.config_list[i]

        #         for j in range(0, len(scheduler.GPU_list[i])):
        #             if len(scheduler.GPU_list[i][j]) == 1:
        #                 if isinstance(scheduler.GPU_list[i][j][0], online_job):
        #                     continue
        #                 if isinstance(scheduler.GPU_list[i][j][0], offline_job):
        #                     self.caculate_completion_time(scheduler.GPU_list[i][j][0], configs[j])
                    
        #             else:
        #                 if isinstance(scheduler.GPU_list[i][j][0], online_job):
        #                     self.caculate_completion_time_concurrency(scheduler.GPU_list[i][j][1], scheduler.GPU_list[i][j][0] ,configs[j])
        #                 else:
        #                     self.caculate_completion_time_concurrency(scheduler.GPU_list[i][j][0], scheduler.GPU_list[i][j][1] ,configs[j])
            

        #     num = 0
        #     job_list = []
          
        #     c = 0
            
        #     while True:
        #         num = num + 1
                
        #         for i in range(0, len(scheduler.GPU_list)):
                 
        #             remove_jobs = []
        #             for j in range(0, len(scheduler.GPU_list[i])):
        #                 if len(scheduler.GPU_list[i][j]) == 1:
        #                     if isinstance(scheduler.GPU_list[i][j][0], offline_job):
        #                         scheduler.GPU_list[i][j][0].progress = scheduler.GPU_list[i][j][0].progress + scheduler.GPU_list[i][j][0].speed
        #                         if scheduler.GPU_list[i][j][0].progress >= scheduler.GPU_list[i][j][0].epoch:
        #                             remove_jobs.append(scheduler.GPU_list[i][j][0])
        #                 else:
        #                     if isinstance(scheduler.GPU_list[i][j][0], offline_job):
        #                         scheduler.GPU_list[i][j][0].progress = scheduler.GPU_list[i][j][0].progress + scheduler.GPU_list[i][j][0].speed
        #                         if scheduler.GPU_list[i][j][0].progress >= scheduler.GPU_list[i][j][0].epoch:
        #                             remove_jobs.append(scheduler.GPU_list[i][j][0])
        #                             c =  c + 1
        #                     else:
        #                         scheduler.GPU_list[i][j][1].progress = scheduler.GPU_list[i][j][1].progress + scheduler.GPU_list[i][j][1].speed
        #                         if scheduler.GPU_list[i][j][1].progress >= scheduler.GPU_list[i][j][1].epoch:
        #                             remove_jobs.append(scheduler.GPU_list[i][j][1])
        #                             c =  c + 1

        #             if len(remove_jobs) != 0:
        #                 for z in remove_jobs:
                           
        #                     z.end_time = num
        #                     job_list.append(z)
                         
        #                     scheduler.state_change(i,z)
                     
                       
        #                 for j in range(0, len(scheduler.GPU_list)):
                        
        #                     for z in range(0, len(scheduler.GPU_list[j])):
        #                         if len(scheduler.GPU_list[j][z]) == 1:
        #                             if isinstance(scheduler.GPU_list[j][z][0], online_job):
        #                                 continue
        #                             if isinstance(scheduler.GPU_list[j][z][0], offline_job):
        #                                 if  scheduler.GPU_list[j][z][0].start_time == -1:
        #                                     scheduler.GPU_list[j][z][0].start_time = num
                    
        #                                 self.caculate_completion_time(scheduler.GPU_list[j][z][0], scheduler.config_list[j][z])
                    
        #                         else:
        #                             if isinstance(scheduler.GPU_list[j][z][0], online_job):
        #                                 if  scheduler.GPU_list[j][z][1].start_time == -1:
        #                                     scheduler.GPU_list[j][z][1].start_time = num
        #                                 self.caculate_completion_time_concurrency(scheduler.GPU_list[j][z][1], scheduler.GPU_list[j][z][0], scheduler.config_list[j][z])
        #                                 c = c + 1
        #                             else:
        #                                 if  scheduler.GPU_list[j][z][0].start_time == -1:
        #                                     scheduler.GPU_list[j][z][0].start_time = num
        #                                 self.caculate_completion_time_concurrency(scheduler.GPU_list[j][z][0], scheduler.GPU_list[j][z][1], scheduler.config_list[j][z])
        #                                 c = c + 1
       
        #         if len(job_list) == self.num:
        #             # for i in job_list:
        #             #     print(i)
            
        #             break
            # self.caculate_system_metrics(jobs=job_list)


    def caculate_completion_time(self, offline_job, config):
        global job_list
        for i in job_list:

            if i.model_name == offline_job.model_name  and config == i.config:
                if is_float(i.average_time):
                    
                    offline_job.speed = 1/float(i.average_time)
                    break
                else:
                    offline_job.speed = 0
    
    def caculate_completion_time_concurrency(self, offline_job:offline_job, online_job:online_job, config):

        online_MPS, offline_MPS = find_optimal_SM(online_job, offline_job, config)
        min = 0 
        for i in throught_list[config]:
            if i[0] == offline_job.model_name and i[2] == online_job.model_name and int(i[3]) == int(online_job.batch_Size) and int(offline_MPS) == int(i[1]) and int(online_MPS) == int(i[4]):
                if is_float(i[5]) and is_float(i[6]):
                    speed = 1/float(i[5])
                    if speed >= min:
                        min = speed
                        offline_job.speed = speed
                    else:
                        continue

    def caculate_system_metrics(self, jobs):
        avarage_queue_time = 0
        JCT = 0
        makespan = 0
        num = len(jobs)
        JCT_list = []
        for i in jobs:
            avarage_queue_time = avarage_queue_time + int(i.start_time) - int(i.submit_time)
            JCT = JCT + int(i.end_time) - int(i.submit_time)
            JCT_list.append(int(i.end_time) - int(i.submit_time))
            if int(i.end_time) > makespan:
                makespan = i.end_time
        

        avarage_queue_time = avarage_queue_time/num
        JCT = JCT/num

        print("avarage_queue_time : ", avarage_queue_time)
        print("JCT: ", JCT)
        print("makespan: ", makespan)
        return JCT_list
    def simulate_executor(self, job):

        job.gi_id = job.new_gi_id
        # for i in range(0, len(node.GPU_list)):
        #     for j in node.GPU_list[i]:
        #         if len(node.GPU_list[i][j]) == 1:
        #             node.GPU_list[i][j][0].gi_id = node.GPU_list[i][j][0].new_gi_id
                
        #         if len(node.GPU_list[i][j]) == 2:
        #             node.GPU_list[i][j][0].gi_id = node.GPU_list[i][j][0].new_gi_id
        #             node.GPU_list[i][j][1].gi_id = node.GPU_list[i][j][1].new_gi_id

    def get_minworkload(self, node):
        if self.algorithm == 'me':
            for i in range(0, len(node.GPU_list)):
                self.busy[i] = calculate_busy_simulator(node.config_list[i], node.GPU_list[i])
        
        min_index = -1
        min = 10000000000
        for i in range(0, len(node.GPU_list)):
            if self.busy[i] < min :
                min = self.busy[i] 
                min_index = i

        if self.algorithm == 'miso':
            num = 10
            min_index = -1
            for i in range(0, len(node.GPU_list)):
                job_num = 0 
                for j in range(0, len(node.GPU_list[i])):
                    job_num =  job_num + len(node.GPU_list[i][j])
                if job_num < num:
                    num = job_num
                    min_index = i

        return min_index

    def state_change(self, node, gpu_index,  job):
        for i in range(0, len(node.GPU_list)):
            for j in range(0 , len(node.GPU_list[i])):
                if job in node.GPU_list[i][j]:
                    gpu_index = i
                    break


        
        for i in node.GPU_list[gpu_index]:
            if job in i:
                index = i.index(job)
                if len(i) >= 2:
                    i.remove(job)
                else:
                    node.GPU_list[gpu_index].remove(i)
                    del node.config_list[gpu_index][index] 
            
                break
        

        jobs = []
        for i in node.GPU_list[gpu_index]:
                for j in i:
                    jobs.append(j)
        

        throught_put, best_config_migrate = node.partition_optimizer(jobs, gpu_index)
        node.throughput[gpu_index] = throught_put

        if not self.job_queue.empty():
            item = self.job_queue.queue[0] 
            gpu_id = self.get_minworkload(node)
            if node.simulator_schedule(item, gpu_id):
                    item = self.job_queue.get()
                    self.simulate_executor(item)

def offline_job_generator(num):
    
    # job_list = ["GAN","transformer","bert","resnet50","resnet152","mobilenet","deeplabv3","SqueezeNet","unet","vit"]
    job_list = ["GAN","resnet50","bert"] 
    epoch_num = [100,200,300]
    offline_job_list = []
    for i in range(0, num):
        # random_ID = random.randint(1, 1000000)
        random_model = random.choice(job_list)
        random_epoch = random.choice(epoch_num)
        random_epoch = random.randint(10, 1000)
        offline_job_list.append(offline_job(random_model, batch_Size=None, epoch=random_epoch))
    return offline_job_list

def online_job_generator(num):
    global job_list
    online_job_list = []
    # job_name_list = ['alexnet', 'bert', 'deeplabv3', 'inception_v3', 'mobilenet_v2', 'resnet50', 'resnet101', 'resnet152', 'unet', 'vgg16', 'vgg19']
    job_name_list  = ["bert","resnet152","resnet50","vgg19","mobilenet_v2"]
    base_size_list = [32]
    config_map = {7:"1c-7g-80gb", 4:"1c-4g-40gb", 3:"1c-3g-40gb", 2:"1c-2g-20gb", 1:"1c-1g-10gb"}
    node = woker()

    for i in range(0, num):
        qos = [40,50,60,70,80,90,100,110,120,130,140,150,160,170]
       
        while True:
            random_batch = random.choice(base_size_list)
            random_model = random.choice(job_name_list)
            random_qos = random.choice(qos)

            flag = False
            online_job_item = online_job(model_name=random_model, batch_Size=random_batch, qos=random_qos)
            if node.best_fit(online_job=online_job_item) != 100:
                config_id = node.best_fit(online_job=online_job_item)
                config  = config_map.get(config_id)
                
                for j in job_list:
                    if j.batch_Size == None :
                        continue
             
                    if j.model_name == online_job_item.model_name and int(j.batch_Size)== int(online_job_item.batch_Size) and j.config == config:
                        if float(j.average_time) * 1000/online_job_item.qos < 0.7:
                            online_job_list.append(online_job_item)
                            flag = True
                            break
                        else:
                            break
            if flag:
                break  
                            
    return online_job_list

# for i in job_list:
#     print(i)
# gpu_num = 16
# offline_jobs = offline_job_generator(100)
# online_jobs = online_job_generator(20)

# test =  I_sheduler()
# for i in online_jobs:
#     print(i, i.qos, test.best_fit(online_job=i))
 


# test = simulator(GPU_num=gpu_num, algorithm='miso', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))


# test = simulator(GPU_num=gpu_num, algorithm='miso', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))
# # test = simulator(GPU_num=gpu_num, algorithm='me', cluster_algorithm='utilizaiton', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))
# test2 = simulator(GPU_num=gpu_num, algorithm='miso', cluster_algorithm='number_of_job_with_resource', online_jobs= copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))

# test = simulator(GPU_num=gpu_num, algorithm='me', cluster_algorithm='number_of_job_with_resource', online_jobs=copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))








# test3 = simulator(GPU_num=gpu_num, algorithm='me_with_over_resource', cluster_algorithm='number_of_job_with_resource', online_jobs= copy.deepcopy(online_jobs), offline_jobs=copy.deepcopy(offline_jobs), num=len(offline_jobs))

