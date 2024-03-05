import glob
import json
import psutil
from datetime import datetime
class job:
    def __init__(self, model_name, config, batch_Size, average_time, tail, jobid=0):
        self.model_name = model_name
        self.config = config
        self.batch_Size = batch_Size
        self.average_time = average_time
        self.tail = tail
        self.jobid = jobid
    def __str__(self):
        return f"Model Name: {self.model_name} Config: {self.config} Batch Size: {self.batch_Size} Average Time: {self.average_time} Tail: {self.tail}"


class online_job:
    def __init__(self, model_name, batch_Size, qos, jobid=0):
        self.new_gi_id =-1
        self.gi_id = -1 
        self.model_name = model_name
        self.batch_Size = batch_Size
        self.qos = qos
        self.jobid = jobid

    def __str__(self):
        return f"online Model Name: {self.model_name}  Batch Size: {self.batch_Size} QOS : {self.qos}"

class offline_job: 
    def __init__(self, model_name, batch_Size, epoch, jobid=0):
        self.new_gi_id =-1
        self.gi_id = -1
        self.model_name = model_name
        self.batch_Size = batch_Size
        self.epoch = epoch
        self.jobid = jobid


def get_throught_single_list():
    path = './jobs/profile/result/single_standardlized'
    job_list = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            lines = line.split(" ")
            job_list.append(lines)
    f.close()
    return job_list

def get_job_list():
    job_list = []
    dir = './jobs/profile/offline_result/'
    file_list = glob.glob(dir+"*")

    for file_name in file_list:
        with open(file_name, 'r') as f:
            file_name = file_name.replace("./jobs/profile/offline_result/", "")

            model_name = file_name
  
            for line in f:
                results = line.split(" ")
                tep_job = job(model_name= model_name, config=results[0], batch_Size=None, average_time=results[1].strip(), tail=None)
                job_list.append(tep_job)
    
        f.close()
    
    dir = './jobs/profile/online_result/'
    file_list = glob.glob(dir+"*")
    for file_name in file_list:
        with open(file_name, 'r') as f:
            file_name = file_name.replace("./jobs/profile/online_result/", "")

            model_name = file_name
            for line in f:
                results = line.split(" ")
                tep_job = job(model_name= model_name, config=results[0], batch_Size=int(results[2].strip()), average_time=results[3].strip(), tail=None)
                job_list.append(tep_job)
    
        f.close()

    return job_list

def generate_jobid(jobs, path = './configs/Job_id.json'):
    
    id_table ={}
    id = 0
    for i in jobs:
        name = ''
        if isinstance(i, online_job):
            name = name +'online_' + i.model_name + '_' + str(i.batch_Size) + '_' + str(i.qos)
            id_table[id] = name

        if isinstance(i, offline_job):
            name = name + 'offline_' +i.model_name + '_' + str(i.epoch)
            id_table[id] = name
        id = id + 1
    with open(path, 'w') as file:
        json.dump(id_table, file, indent=4)
    
def generate_jobs(path = './configs/Job_id.json'):
    jobs = []
    with open(path, 'r') as file:
        data = json.load(file)
    
    for i in data.keys():
        information = data[i].split("_")
        if information[0] == 'online':
            jobs.append(online_job(model_name=information[1], batch_Size=int(information[2]), qos=int(information[3]), jobid=int(i)))
        if information[0] == 'offline':
            jobs.append(offline_job(model_name=information[1], epoch=int(information[2]), batch_Size=None, jobid=int(i)))
    

    return jobs

def generate_job_progress_table(jobs, path='./configs/jobs.json'):
    progress_table = {}
    for i in jobs:
        name = ''
        if isinstance(i, online_job):
        
            name = 0
            progress_table[i.jobid] = name

        if isinstance(i, offline_job):
            name = 0
            progress_table[i.jobid] = name
    with open(path, 'w') as file:
            json.dump(progress_table, file, indent=4)
    
def read_job_progress(jobid, path):
    with open(path + './configs/jobs.json', 'r') as file:
        data = json.load(file)
    return data[str(jobid)]

def record_job_progress(jobid, progress, path):
    
    with open(path + './configs/jobs.json', 'r') as file:
        data = json.load(file)
    
    data[str(jobid)] = progress

    with open('./configs/jobs.json', 'w') as file:
        json.dump(data, file, indent=4)


def get_job(job_id, path = './configs/Job_id.json'):
    job = None
    with open(path, 'r') as file:
        data = json.load(file)
    
    for i in data.keys():
        if int(i) == int(job_id):
            information = data[i].split("_")
            if information[0] == 'online':
                job = online_job(model_name=information[1], batch_Size=int(information[2]), qos=int(information[3]), jobid=int(i))
            if information[0] == 'offline':
                job = offline_job(model_name=information[1], epoch=int(information[2]), batch_Size=None, jobid=int(i))


    return job




import random
from collections import deque
from itertools import product



class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.flag = False
        self.father = None
    
    def traverse_children(self):
        queue = deque([self])
        while queue:
            current = queue.popleft()
            current.flag = True
            queue.extend(current.children)
    
    def add_children(self, TreeNode):
        self.children.append(TreeNode)
    
    def set_father(self, TressNode):
        self.father = TressNode

    def remove_children(self, TreeNode):
        self.children.remove(TreeNode)
    
    def change_father(self):
       
        if self.father != None:
            self.father.flag = True
            self.father.change_father()







root = TreeNode(value=0)
layer2_node1 = TreeNode(value=1)
layer2_node2 = TreeNode(value=2)
layer3_node1 = TreeNode(value=3)
layer3_node2 = TreeNode(value=4)
layer3_node3 = TreeNode(value=5)
layer4_node1 = TreeNode(value=7)
layer4_node2 = TreeNode(value=8)
layer4_node3 = TreeNode(value=9)
layer4_node4 = TreeNode(value=10)
layer4_node5 = TreeNode(value=11)
layer4_node6 = TreeNode(value=12)
layer4_node7 = TreeNode(value=13)


root.add_children(layer2_node1)
root.add_children(layer2_node2)
layer2_node1.set_father(root)
layer2_node2.set_father(root)

layer2_node1.add_children(layer3_node1)
layer2_node1.add_children(layer3_node2)
layer3_node1.set_father(layer2_node1)
layer3_node2.set_father(layer2_node1)

layer2_node2.add_children(layer3_node3)
layer2_node2.add_children(layer4_node7)
layer3_node3.set_father(layer2_node2)
layer4_node7.set_father(layer2_node2)

layer3_node1.add_children(layer4_node1)
layer3_node1.add_children(layer4_node2)
layer4_node1.set_father(layer3_node1)
layer4_node2.set_father(layer3_node1)

layer3_node2.add_children(layer4_node3)
layer3_node2.add_children(layer4_node4)
layer4_node3.set_father(layer3_node2)
layer4_node4.set_father(layer3_node2)

layer3_node3.add_children(layer4_node5)
layer3_node3.add_children(layer4_node6)
layer4_node5.set_father(layer3_node3)
layer4_node6.set_father(layer3_node3)


config_choice_list = {
    '1c-1g-10gb': [13,11,12,7,8,9,10],
    '1c-2g-20gb': [5,3,4],
    '1c-3g-40gb': [2,1],
    '1c-4g-40gb': [1],
    '1c-7g-80gb': [0]
}

TreeNode_map = {
    0 : root,
    1 : layer2_node1,
    2 : layer2_node2,
    3 : layer3_node1,
    4 : layer3_node2,
    5 : layer3_node3,
    7 : layer4_node1,
    8 : layer4_node2,
    9 : layer4_node3,
    10 : layer4_node4,
    11 : layer4_node5,
    12 : layer4_node6,
    13 : layer4_node7,
}

MIG_instance_map = {
    '1g.10gb': 19,
    '2g.20gb': 14,
    '3g.40gb': 9,
    '4g.40gb': 5,
    '7g.80gb': 0,
}


config_map = {
        '1c-1g-10gb': 1,
        '1c-2g-20gb': 2,
        '1c-3g-40gb': 3,
        '1c-4g-40gb': 4,
        '1c-7g-80gb' : 7,
 }
reversed_config_map = {
    1: '1c-1g-10gb',
    2: '1c-2g-20gb',
    3: '1c-3g-40gb',
    4: '1c-4g-40gb',
    7: '1c-7g-80gb',
}


def clean_tree():
    for i in TreeNode_map.keys():

        node = TreeNode_map.get(i)
        node.flag = False

def check_volid(config, online_jobs, online_config):

    gi_id_list = []

    
    for i in range(0, len(online_jobs)):
        if online_jobs[i].gi_id != -1 :

            gi_id_list.append(int(online_jobs[i].gi_id))
            
            config.remove(online_config[i])
    for i in gi_id_list:
        node = TreeNode_map.get(i)
        node.flag = True
        node.change_father()
        node.traverse_children()



    reverse_list = sorted(config, reverse=True)

    for i in reverse_list:
        config = reversed_config_map.get(i)
        find = False
        for j in config_choice_list.get(config):
            node = TreeNode_map.get(j)
            if node.flag == False:
                find = True
                node.flag = True
                node.change_father()
                node.traverse_children()
                break
            else:
                continue
        if not find:
            clean_tree()
            return False
    
    clean_tree()
    return True

def check_available(gi_id, used_list):
    for i in used_list:
        node = TreeNode_map.get(int(i))
        node.flag = True
        node.change_father()
        node.traverse_children()
    
    node = TreeNode_map.get(int(gi_id))
    if node.flag == True:
        clean_tree()
        return False
        
    else:   
        clean_tree()
        return True
    
def set_gi_id(jobs, config):
 
    config_reserve = []
    for i in config:
        config_reserve.append(config_map.get(i))

    zipped_pairs = sorted(zip(config_reserve, jobs), key=lambda x: x[0], reverse=True)
    sorted_list1, sorted_list2 = zip(*zipped_pairs)
    config_reverse = list(sorted_list1)
    jobs_reverse = list(sorted_list2)

    index_list = [] 

    for i in range(0, len(jobs_reverse)):
        if len(jobs_reverse[i]) == 1:
            if isinstance(jobs_reverse[i][0], online_job):
                if jobs_reverse[i][0].new_gi_id != -1:
                    node  = TreeNode_map.get(int(jobs_reverse[i][0].new_gi_id))
                    node.flag = True
                    node.change_father()
                    node.traverse_children()
                    index_list.append(i)
        
        else:
            if isinstance(jobs_reverse[i][0], online_job):
                if jobs_reverse[i][0].new_gi_id != -1:
                    node  = TreeNode_map.get(int(jobs_reverse[i][0].new_gi_id))
                    node.flag = True
                    node.change_father()
                    node.traverse_children()
                    index_list.append(i)

            elif isinstance(jobs_reverse[i][1], online_job):
                if jobs_reverse[i][1].new_gi_id != -1:
                    node  = TreeNode_map.get(int(jobs_reverse[i][1].new_gi_id))
                    node.flag = True
                    node.change_father()
                    node.traverse_children()
                    index_list.append(i)
  
    for i in range(0, len(jobs_reverse)):
        config = reversed_config_map.get(config_reverse[i])
        if i in index_list:
            continue
        
        new_gi_id = -1
        choice_list_copy = config_choice_list.get(config).copy()

        for j in choice_list_copy:

            node = TreeNode_map.get(int(j))
            if node.flag == False:
                node.flag = True
                new_gi_id = node.value
                node.change_father()
                node.traverse_children()
                break
            else:
                continue
        
        # if len(jobs_reverse[i]) == 1 and isinstance(jobs_reverse[i][0], offline_job):
        #     for j in config_choice_list.get(config):
        #         node = TreeNode_map.get(j)
        #         if node.flag == False:
        #             node.flag = True
        #             new_gi_id = node.value
        #             node.change_father()
        #             node.traverse_children()
        #             break
        #         else:
        #             continue
        
        # else:
        #     choice_list_copy = config_choice_list.get(config).copy()
        #     # choice_list_copy.reverse()
        #     # random.shuffle(choice_list_copy)
        #     for j in choice_list_copy:
        #         node = TreeNode_map.get(j)
        #         if node.flag == False:
        #             find = True
        #             node.flag = True
        #             new_gi_id = node.value
        #             node.change_father()
        #             node.traverse_children()
        #             break
        #         else:
        #             continue
   
        if len(jobs_reverse[i]) == 2:
            jobs_reverse[i][0].new_gi_id = new_gi_id
            jobs_reverse[i][1].new_gi_id = new_gi_id

        else:
            jobs_reverse[i][0].new_gi_id = new_gi_id
    clean_tree()

def search_check_volid(gi_id_list):
    for i in gi_id_list:
        node = TreeNode_map.get(int(i))
        if node.flag == True:
            clean_tree()
            return False
        
        else:   
            node.flag = True
            node.change_father()
            node.traverse_children()
    clean_tree()
    return True


def evalute_solution(gi_id_list, jobs):

    for i in range(0, len(gi_id_list)):
        if isinstance(jobs[i], online_job):
            node = TreeNode_map.get(int(gi_id_list[i]))
            node.flag = True
            node.change_father()
            node.traverse_children()


    for i in range( len(config_choice_list.keys()) - 1 ,-1, -1):
        for j in config_choice_list.get(list(config_choice_list.keys())[i]):
            node = TreeNode_map.get(j)
            if node.flag == False:
                clean_tree()
                return config_map.get(list(config_choice_list.keys())[i])
            
            else:
                continue
    
    
    clean_tree()
    return 0

def search_solution(jobs, config):
    num = len(config)
    config_reserve = []
    for i in config:
        config_reserve.append(config_map.get(i))

    zipped_pairs = sorted(zip(config_reserve, jobs), key=lambda x: x[0], reverse=True)
    sorted_list1, sorted_list2 = zip(*zipped_pairs)
    config_reverse = list(sorted_list1)
    jobs_reverse = list(sorted_list2)

    
    search_list = []

    for i in range(0, len(config_reverse)):
        if len(jobs_reverse[i]) == 1:
            if isinstance(jobs_reverse[i][0], online_job) and jobs_reverse[i][0].gi_id != -1:
                tmp_config = []
                tmp_config.append(jobs_reverse[i][0].gi_id)
                search_list.append(tmp_config)
                continue
            config  = reversed_config_map.get(config_reverse[i])
            config = config_choice_list.get(config).copy()
            search_list.append(config)
        
        else:
            if isinstance(jobs_reverse[i][0], online_job) and jobs_reverse[i][0].gi_id != -1:
                tmp_config = []
                tmp_config.append(jobs_reverse[i][0].gi_id)
                search_list.append(tmp_config)
                continue

            elif isinstance(jobs_reverse[i][1], online_job) and jobs_reverse[i][1].gi_id != -1:
                tmp_config = []
                tmp_config.append(jobs_reverse[i][1].gi_id)
                search_list.append(tmp_config)
                continue

            config  = reversed_config_map.get(config_reverse[i])
            config = config_choice_list.get(config).copy()
            search_list.append(config)

        

    combinations = list(product(*search_list))
   
    volid_solution = []
  
    for i in combinations:
        if search_check_volid(i):
            volid_solution.append(i)
    
    
    MAX_resource = -1
    solution = []

    for i in volid_solution:
        i = list(i)
        result = evalute_solution(i, jobs_reverse)
        if result >= MAX_resource:
            MAX_resource = result
            solution = i
    


    for i in range(0, len(jobs_reverse)):
        if len(jobs_reverse[i]) == 1:
            if isinstance(jobs_reverse[i][0], online_job) and jobs_reverse[i][0].gi_id == -1:
                jobs_reverse[i][0].gi_id = solution[i]
        else:
            if isinstance(jobs_reverse[i][0], online_job) and jobs_reverse[i][0].gi_id == -1:
                jobs_reverse[i][0].gi_id = solution[i]
            if isinstance(jobs_reverse[i][1], online_job) and jobs_reverse[i][0].gi_id == -1:  
                jobs_reverse[i][1].gi_id = solution[i]

    clean_tree()


def check_speedup(offline_job, config):
    dir = '/data/zbw/MIG/MIG/ATC-MIG/jobs/profile/offline_result/'
    config_list = ['1c-1g-10gb', '1c-2g-20gb', '1c-3g-40gb', '1c-4g-40gb', '1c-7g-80gb']
    path = dir + offline_job.model_name
    index = config_list.index(config)
    ori_speed = 0
    pri_speed = 0
    speed_up = 0
    resource_speed  = 0

    with open(path, 'r') as file:
        for line in file:
            lines = line.strip().split(" ")
            if lines[0] == config:
                
                ori_speed = lines[1]
            if lines[0] == config_list[index-1]:
              
                pri_speed = lines[1]
    file.close()


    resource_speed  = config_map.get(config)/ config_map.get(config_list[index-1])
  
    if pri_speed == 'error':
        return True
    
    speed_up = (float(pri_speed))/float(ori_speed)

    if speed_up/resource_speed >= 1:
        return True
    else:
        return False

def calculate_utilization(job, config, monitor_result):
    dir = '/data/zbw/MIG/MIG/ATC-MIG/jobs/profile/offline_profile/'
    utilization = 0  
    if isinstance(job, online_job):
        dir = '/data/zbw/MIG/MIG/ATC-MIG/jobs/profile/online_profile/'
        path = dir + job.model_name

        with open(path, 'r') as file:
            lines = file.readlines()  # 读取所有行到一个列表中
            lines.reverse()
         
            for line in lines:
                result = line.strip().split(" ")
                MIG_config = result[0].split("+")[0]
                SM = float(result[0].split("+")[1])
                if result[3] != 'error' and MIG_config == config and float(result[3]) * 1000 < job.qos:
                    file.close()
                    return SM/100
                
        file.close()

    else:
        utilization = monitor_result

    return utilization 

def calculate_busy(config_list, gpu_list, monitor_result):
    utilization = 0

    for i in range(0, len(config_list)):
        
        A100_percnetage = config_map.get(config_list[i])/7
        MIG_utilizaiton = 0

        if len(gpu_list[i]) == 2:

            MIG_utilizaiton = 1 

        else:
            if isinstance(gpu_list[i][0], offline_job):
                if config_map.get(config_list[i]) == 1:
                    MIG_utilizaiton = 1
                elif check_speedup(gpu_list[i][0], config_list[i]):
                    MIG_utilizaiton = 1
                else:
                    GI_ID = gpu_list[i][0].gi_id
                    if int(GI_ID) not in monitor_result.keys():
                        monitor_result[int(GI_ID)] = 0 
                    MIG_utilizaiton = calculate_utilization(gpu_list[i][0], config_list[i], monitor_result[int(GI_ID)])
            else:
                GI_ID = gpu_list[i][0].gi_id
                if int(GI_ID) not in monitor_result.keys():
                    monitor_result[int(GI_ID)] = 0 
                MIG_utilizaiton = calculate_utilization(gpu_list[i][0], config_list[i], monitor_result[int(GI_ID)])
   
        utilization = utilization + MIG_utilizaiton * A100_percnetage

    return utilization


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def get_throughput_double_list():
    throught_list = {}
    file_path = './jobs/profile/result/2'
    num = 0 
    with open(file_path, 'r') as f:
        item = ''
        config  = ''
        offline = ''
        offline_MPS =  0
        offline_runtime = 0
        online = ''
        online_batch = 0
        online_MPS = 0
        online_runtime = 0
        for line in f:
            results = line.split(" ")
            if results[0] == 'offline':
                config = results[1]
                offline = results[2]
                offline_MPS = int(results[3])
                if results[7].strip() != 'error':
                    offline_runtime = float(results[7].strip())
                else:
                    offline_runtime = 'error'
        
            if results[0] == 'online':
                online = results[2]
                online_batch = int(results[3])
                online_MPS = int(results[4])
                if is_float(results[7]):
                    online_runtime = float(results[7]) * 1000
                else:
                    online_runtime = 'error'
            num = num + 1
            if config  not in throught_list.keys():
                throught_list[config]  = []
            if num % 2 ==0:
                tmp_item  = []
                tmp_item.append(offline)
                tmp_item.append(offline_MPS)
                tmp_item.append(online)
                tmp_item.append(online_batch)
                tmp_item.append(online_MPS)
                tmp_item.append(offline_runtime)
                tmp_item.append(online_runtime)
                throught_list[config].append(tmp_item)

    f.close()
    
    return throught_list


def check_process_running(pid):
    if psutil.pid_exists(pid):
        process = psutil.Process(pid)
        if process.is_running():
            return True
    return False



def handle_job_log():
    log_path = '/data/zbw/MIG/MIG/ATC-MIG/log/job_log'
    job_path = '/data/zbw/MIG/MIG/ATC-MIG/configs/Job_id.json'
    job_list = generate_jobs()
    

    time_table = {}

    offline_job_list = []
    for i in job_list:
        if isinstance(i, offline_job):
            offline_job_list.append(i)
            time_table[i.jobid] = {}




    for i in offline_job_list:

        with open(log_path, 'r') as file:
            for line in file:
                fields = line.split()
                timestamp_str = fields[0] + ' ' + fields[1]
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                identifier = int(fields[2])
                action = fields[3]
                if int(identifier) == int(i.jobid):
                    if action == 'finish':
                        time_table[i.jobid]['end_time'] = timestamp

                    if action == 'start':
                        if 'start' not in time_table[i.jobid].keys():
                            time_table[i.jobid]['start'] = timestamp

        file.close()  
    


    JCT = 0
    makespan = 0
    start_time = '2024-04-04 00:00:00'
    end_time = '2023-09-01 00:20:10'


    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    for i in time_table.keys():
        JCT = JCT +  (time_table[i]['end_time'] -  time_table[i]['start']).total_seconds()
    JCT = JCT/len(offline_job_list)
    

    for i in time_table.keys():
        if time_table[i]['start'] < start_time:
            start_time = time_table[i]['start']
        if time_table[i]['end_time'] > end_time:
            end_time = time_table[i]['end_time']
    makespan =  end_time - start_time
    
    print("MakeSpan: " + str(makespan.total_seconds()))
    print("JCT: " + str(JCT))


    