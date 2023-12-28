import subprocess
import os
import signal
import time
import threading
import grpc
import grpc_tool.server_scherduler_pb2_grpc as server_scherduler_pb2_grpc
import grpc_tool.server_scherduler_pb2 as  server_scherduler_pb2 
import util.MIG_operator as MIG_operator
from concurrent import futures
from util.sharing import *
import socket
from itertools import permutations
from threading import Lock

temp_lock = Lock()
busy_table ={

}
busy = []
UUID_table = {

}

static_partition = {

}

monitor_table = {

}


ip='10.16.56.14'
port=50052
node = socket.gethostname()
num_GPU = 1
online_job_data = []
config_map = {7:"1c-7g-80gb", 4:"1c-4g-40gb", 3:"1c-3g-40gb", 2:"1c-2g-20gb", 1:"1c-1g-10gb"}
global_config_list = [[7], [4,3], [4,2,1], [4,1,1,1], [3,3], [3,2,1], [3,1,1,1],[2,2,3], [2,1,1,3], [1,1,2,3], [1,1,1,1,3], [2,2,2,1], [2,1,1,2,1],[1,1,2,2,1],[2,1,1,1,1,1],
                   [1,1,2,1,1,1], [1,1,1,1,2,1], [1,1,1,1,1,2], [1,1,1,1,1,1,1]]
reverser_map = {"1c-7g-80gb" : 7, "1c-4g-40gb": 4, "1c-3g-40gb":3, "1c-2g-20gb":2, "1c-1g-10gb":1, "baseline":10}

job_list = get_throught_single_list()

online_job_data = get_job_list()

for i in range(0, num_GPU):
    UUID_table[i] = {

    }

    static_partition[i] = []

    monitor_table[i] = {

    }

    busy_table[i] = {

    }
    busy.append(0)
class woker: 
    def __init__(self, cluster_algorithm='miso', max_job_per_GPU=4):
        self.jobs_pid = {}
        self.fix_job = []
        self.cluster_algorithm = cluster_algorithm
        self.GPU_list = []
        self.config_list = []
        self.throughput = []
        self.max_job_per_GPU = max_job_per_GPU

        for i in range(0, num_GPU):
            self.GPU_list.append([])
            self.throughput.append(0)
            self.config_list.append([])
            self.fix_job.append([])

    def start_update_load(self):
        self.update_thread = threading.Thread(target=self.periodic_load_update)
        self.update_thread.start()

    def node_schedule(self, new_job, gpu_id):
        with temp_lock:
            jobs = []
            for i in self.GPU_list[gpu_id]:
                for j in i:
                    jobs.append(j)
            jobs.append(new_job)
            if self.cluster_algorithm == 'miso':
                if len(jobs) <= self.max_job_per_GPU:
                    if(not self.miso_partition_optimizer(jobs, gpu_id)):
                        return False
                
                    elif isinstance(new_job, offline_job):
                        throught_put = self.miso_partition_optimizer(jobs, gpu_id)
                        if throught_put < self.throughput[gpu_id]:
                            jobs.remove(new_job)
                            self.miso_partition_optimizer(jobs, gpu_id)
                            return False
                        else:
                            self.throughput[gpu_id] = throught_put
                            self.sorted(gpu_id)
                            self.termination(gpu_id)
                            self.creation(gpu_id)
                            time.sleep(20)
                    else:
                        throught_put = self.miso_partition_optimizer(jobs, gpu_id)
                        self.throughput[gpu_id] = throught_put
                    
                        self.sorted(gpu_id)
                        self.termination(gpu_id)
                        self.creation(gpu_id)
                        self.fix_job[gpu_id].append(new_job)
                    time.sleep(20)
                    return True
            
                else:
                    return False
                
            if self.cluster_algorithm == 'me':
                pass

    



    def miso_partition_optimizer(self, jobs, gpu_id):
        ## 
        # this part is used to get jobs from job_ids
        ##
        global global_config_list

        online_jobs = []
        offline_jobs = []

        for i in jobs:
            if isinstance(i, online_job):
                online_jobs.append(i)
            else:
                offline_jobs.append(i)
        online_config = []
        for i in online_jobs:
            online_config.append(self.best_fit(i))
        valid_config = []

        for i in global_config_list:
            valid = True
            if len(i) >= len(online_jobs) + len(offline_jobs):
                tmp = i.copy()
                for j in online_config:
                    if j not in tmp:
                        valid = False
                        break
                    else:
                        tmp.remove(j)
                if valid:
                    valid_config.append(i.copy())


    
        if len(valid_config) == 0:
            return False

        valid = []
       
        for i in valid_config:
            if check_volid(i.copy(), online_jobs, online_config):
                valid.append(i)

   
        valid_config = valid
            

        for i in valid_config:
            for j in online_config:
                i.remove(j)
    
        
        best_obj = 0
        best_config = None
        for i in valid_config:
            n = len(offline_jobs)
            if n == 0 :
                self.GPU_list[gpu_id] = []
                self.config_list[gpu_id] = []
                config_list = []

                for j in jobs:
                    config_list.append(config_map.get(online_config[online_jobs.index(j)]))

                for j in range(0, len(jobs)):
                    self.GPU_list[gpu_id].append([jobs[j]])
                    self.config_list[gpu_id].append(config_list[j])
                    set_gi_id(self.GPU_list[gpu_id], config_list)
                return 0.0000001
          
            all_combinations = list(permutations(i, n))
            for combo in all_combinations:
               
                config = []
               
                for z in combo:
                    config.append(config_map.get(z))
              
                throught =  self.Calculated_throughput(config, offline_jobs)
                
                if throught > best_obj:
                    best_config = config
                    best_obj = throught
                    
        config_list = []
        self.GPU_list[gpu_id] = []
        for i in jobs:
            if isinstance(i, online_job):
                config_list.append(config_map.get(online_config[online_jobs.index(i)]))
                self.GPU_list[gpu_id].append([i])
            if isinstance(i, offline_job):
                self.GPU_list[gpu_id].append([i])
                config_list.append(best_config[offline_jobs.index(i)])

        set_gi_id(self.GPU_list[gpu_id], config_list)

        self.config_list[gpu_id] = config_list

        return best_obj

    def best_fit(self, online_job):
        global online_job_data
        MIG_partition_list = []
        for i in online_job_data:
            if i.average_time == 'error' or i.batch_Size ==  None:
                continue
            if i.model_name == online_job.model_name and int(i.batch_Size)== int(online_job.batch_Size) and float(i.average_time) * 1000 < online_job.qos:
                MIG_partition_list.append(i.config)

        min = 100
        for i in range(0, len(MIG_partition_list)):
            GI = reverser_map[MIG_partition_list[i]]
            if GI:
                if GI <= min:
                    min = GI

        return min
    
    def Calculated_throughput(self, config_list, jobs):
       
        throughput = 0
        global job_list
        
        for i in job_list:
            if i[2] == 'error':
                continue
            for j in range(0, len(jobs)):
                if jobs[j].model_name == i[0]  and config_list[j] == i[1]:
                    throughput = throughput + float(i[2])                
    
        return throughput
    

    def termination(self, gpu_id):
        try:
            for i in self.GPU_list[gpu_id]:
                if len(i) == 1:
                    if i[0] not in self.fix_job[gpu_id]:
                        if i[0].jobid not in self.jobs_pid.keys():
                            continue
                        pid = self.jobs_pid[i[0].jobid]
                        os.kill(pid, signal.SIGTERM) 

                if len(i) == 2:
                    if i[0] not in self.fix_job[gpu_id]:
                        if i[0].jobid not in self.jobs_pid.keys():
                            continue
                        pid = self.jobs_pid[i[0].jobid]
                        os.kill(pid, signal.SIGTERM) 
                    if i[1] not in self.fix_job[gpu_id]:
                        if i[1].jobid not in self.jobs_pid.keys():
                            continue
                        pid = self.jobs_pid[i[1].jobid]
                        os.kill(pid, signal.SIGTERM)
        except Exception as e:
            print('pid missing')
        time.sleep(3)


        fix_partition = []
        destory_partition = []

        for i in self.fix_job[gpu_id]:
            fix_partition.append(i.gi_id)

        for i in UUID_table[gpu_id].keys():
            
            if int(UUID_table[gpu_id][i]) not in fix_partition:

                destory_partition.append(UUID_table[gpu_id][i])
        
        for i in destory_partition:
            stop_monitor(gpu_id=gpu_id, GI_ID=i)
            MIG_operator.destroy_ins(gpu_id, i)
            update_uuid(gpu_id, i, 'destroy')

    def creation(self, gpu_id):
        type = 'create'
        for i in range(0, len(self.GPU_list[gpu_id])):
            if len(self.GPU_list[gpu_id][i]) == 1:
                if self.GPU_list[gpu_id][i][0] not in self.fix_job[gpu_id]:
                    if isinstance(self.GPU_list[gpu_id][i][0], offline_job):
                        config = self.config_list[gpu_id][i]
                        ID = MIG_operator.create_ins(gpu_id, config)

                        self.GPU_list[gpu_id][i][0].gi_id = ID
                        update_uuid(gpu_id, ID, type)
                        start_GPU_monitor(gpu_id=gpu_id, GI_ID=ID)
                        UUID = 0
                        for j in UUID_table[gpu_id].keys():
                            if int(UUID_table[gpu_id][j]) == int(ID):
                                UUID = j
                                break
                        self.executor(job=self.GPU_list[gpu_id][i][0], UUID=UUID)

                    else:
                        GI_ID = self.GPU_list[gpu_id][i][0].gi_id
                        config = self.config_list[gpu_id][i]
                        ID = MIG_operator.create_ins_with_ID(gpu_id, config, GI_ID)
                        update_uuid(gpu_id, ID, type)
                        start_GPU_monitor(gpu_id=gpu_id, GI_ID=ID)
                        UUID = 0
                        for j in UUID_table[gpu_id].keys():
                            if int(UUID_table[gpu_id][j]) == int(ID):
                                UUID = j
                                break
                        self.executor(job=self.GPU_list[gpu_id][i][0], UUID=UUID)
                else:
                    GI_ID = self.GPU_list[gpu_id][i][0].gi_id
                    UUID = 0
                    for j in UUID_table[gpu_id].keys():
                        if int(UUID_table[gpu_id][j]) == int(GI_ID):
                            UUID = j
                            break
                    continue
            else:
                pass
    
    def run_process(self, UUID, path, model_name, type, epoch, jobid):
        global ip, port, node
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = server_scherduler_pb2_grpc.SchedulerServiceStub(channel)
            JobState = stub.JobState(server_scherduler_pb2.JobStateMessage(
                    type ='start', JobID = jobid
                ))
            

        env = os.environ.copy()
        env["CUDA_VISIBLE_DEVICES"] = UUID
        if type == "--batch":
            cmd = [
                "python",
                f"{path}entry.py",
                "--task",
                model_name,
                type,
                str(epoch)
            ]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
            self.jobs_pid[jobid] = int(p.pid)
            p.wait()
        

        if type == '--epoch':
            cmd = [
                "proxychains",
                "python",
                f"{path}entry.py",
                "--task",
                model_name,
                type,
                str(epoch),
                '--jobid',
                str(jobid)
            ]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
            self.jobs_pid[jobid] = int(p.pid)
            p.wait()

       
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = server_scherduler_pb2_grpc.SchedulerServiceStub(channel)
         
            if p.returncode == 0:
                with temp_lock:
                    if self.cluster_algorithm == 'miso':
                        gpu_index =-1
                        for i in range(0, len(self.GPU_list)):
                            jobs = []
                            for j in range(0, len(self.GPU_list[i])):
                                for z in self.GPU_list[i][j]:
                                    jobs.append(z)

                            flag = False
                            tmp_job = None
                            for j in jobs:
                                if j.jobid == jobid:
                                    tmp_job = j
                                    gpu_index = i
                                    flag = True
                                    break 
                                
                    jobs.remove(tmp_job)
                    if flag:
                        MIG_operator.destroy_ins(gpu_index, tmp_job.gi_id)
                        self.throughput[gpu_index] = 0
                        self.miso_partition_optimizer(jobs=jobs, gpu_id= gpu_index)
                        self.sorted(gpu_index)
                        self.termination(gpu_index)
                        self.creation(gpu_index)
                    JobState = stub.JobState(server_scherduler_pb2.JobStateMessage(
                        type ='finish', JobID = jobid
                    ))

                    return 0
            
            if p.returncode == 143  or -15:
                JobState = stub.JobState(server_scherduler_pb2.JobStateMessage(
                    type ='pause', JobID = jobid
                ))
    

    def periodic_load_update(self):
        while True:
            self.load_update()
            time.sleep(2)

    def load_update(self):
        global ip, port, node, busy
        for i in range(0, num_GPU):
            busy[i] = calculate_busy(gpu_list=self.GPU_list[i], config_list=self.config_list[i], monitor_result= busy_table[i])

      
        for i in range(0, num_GPU):
            with grpc.insecure_channel(f'{ip}:{port}') as channel:
                stub = server_scherduler_pb2_grpc.SchedulerServiceStub(channel)

                Load = stub.Load(server_scherduler_pb2.LoadInformation(
                    name = node, GPU_ID=i , load = busy[i]
                    ))
  

    
       




    def executor(self, job, UUID, MPS_flag = False, MPS_percentage=None):
        offline_path = './jobs/offline/'
        online_path = './jobs/online/'
        if not MPS_flag:
            if isinstance(job, online_job):
                # cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && python {online_path}entry.py --task {job.model_name} --batch {job.batch_Size}'
                thread = threading.Thread(target=self.run_process, args=(UUID, online_path, job.model_name, '--batch' ,job.batch_Size ,job.jobid))
               
            if isinstance(job, offline_job):
                # cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && python {offline_path}entry.py --task {job.model_name} --epoch {job.epoch}'
                thread = threading.Thread(target=self.run_process, args=(UUID, offline_path, job.model_name, '--epoch' ,job.epoch ,job.jobid))
            thread.start()
        else:
            pass
      

    def sorted(self, gpu_id):
        combined = sorted(zip(self.config_list[gpu_id], self.GPU_list[gpu_id]), key=lambda x: (-reverser_map[x[0]]))
        if combined:
            sorted_list1, sorted_list2 = zip(*combined)
        else:
            sorted_list1, sorted_list2 = [], []
        sorted_list1 = list(sorted_list1)
        sorted_list2 = list(sorted_list2)

        self.config_list[gpu_id] = sorted_list1
        self.GPU_list[gpu_id] = sorted_list2



class GPU_monitor:
    def __init__(self):
        self.running = True
    

    def start_GPU_monitor(self, gpu_id, gi_id):
        while self.running:
            cmd = f'dcgmi dmon -e 1002 -d 1000 -i {gpu_id}/{gi_id}/0'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            start_time = time.time() 
            while self.running and  time.time() - start_time < 3:
                output = process.stdout.readline()
                output = output.strip()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    if len(output.split()) != 3:
                        continue
                    else:
                        busy_table[gpu_id][int(gi_id)] = float(output.split()[2]) 
            process.terminate() 
            process.wait()

    def stop(self):
        self.running = False





def WorkerService():
    regist_worker()
    node = woker()
    node.start_update_load()
    restart_thread = threading.Thread(target=restart_dcgm)
    restart_thread.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_scherduler_pb2_grpc.add_WorkerServiceServicer_to_server(server_scherduler_pb2_grpc.WorkerServiceServicer(node), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def start_GPU_monitor(gpu_id, GI_ID):
    monitor = GPU_monitor()
    monitor_thread = threading.Thread(target=monitor.start_GPU_monitor, args=(gpu_id, GI_ID))
    monitor_thread.start()
    monitor_table[gpu_id][GI_ID] = monitor

def update_uuid(gpu_id, GI_ID, type):
    if type == 'destroy':
        for i in UUID_table[gpu_id].keys():
            if UUID_table[gpu_id][i] == GI_ID:
                del UUID_table[gpu_id][i]
                break
    if type == 'create':
        UUID_list = MIG_operator.get_uuid(gpu_id)
        for i in UUID_list:
            if i not in UUID_table[gpu_id].keys():
                UUID_table[gpu_id][i] = GI_ID
                break


def stop_monitor(gpu_id, GI_ID):
    monitor = monitor_table[gpu_id][GI_ID] 
    monitor.stop()
    time.sleep(1)
    del monitor_table[gpu_id][GI_ID]

def regist_worker():
    global ip, port, node
   
    def get_local_ip():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            return ip
        except Exception as e:
            print(f"Error: {e}")
        return None

    local_ip = get_local_ip()
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = server_scherduler_pb2_grpc.SchedulerServiceStub(channel)

        Regist = stub.Regist(server_scherduler_pb2.NodeInformation(
            name = node, ip = local_ip , port = 50051
            ))



def restart_dcgm():
    while True:
        cmd = f'sudo service nvidia-dcgm restart'
        p = subprocess.Popen([cmd], shell=True)
        p.wait()
        print('dcgm service restart')
        time.sleep(30)
