from util.sharing import *
from concurrent import futures
from log.job_log import *

import grpc
import grpc_tool.server_scherduler_pb2_grpc as server_scherduler_pb2_grpc
import grpc_tool.server_scherduler_pb2 as  server_scherduler_pb2 

import threading
import time
import configs.configs as configs
from collections import deque

job_queue = deque()

class SchedulerObject:
    def __init__(self):
        self.worker_table = {}
        self.load = {}
        self.lock = threading.Lock()

    def add_worker(self, request):
        with self.lock:
            self.worker_table[request.name] = {(request.ip, request.port)}
            self.load[request.name] = {}

    def update_load(self, request):
        with self.lock:
            self.load[request.name][request.GPU_ID] = request.load

    def get_min_load(self):
        min = 100
        min_name = None
        min_GPU_ID = 0
        with self.lock:
            for name in self.load.keys():
                for GPU_ID in self.load[name].keys():
                    if self.load[name][GPU_ID] <= min:
                        min = self.load[name][GPU_ID]
                        min_name = name
                        min_GPU_ID = GPU_ID

        return min_name, min_GPU_ID

    def try_schedule(self):
        if len(job_queue) != 0:
            item = job_queue[0]
            if schedule(item):
                item = job_queue.popleft()
    
Scheduler = SchedulerObject()

def start_service():
    service_thread = threading.Thread(target=SchedulerService)
    service_thread.start()

    time.sleep(5)


    main_thread = threading.Thread(target=start_cluster)
    main_thread.start()

    while True:
        record_node_load(Scheduler.load)
        time.sleep(30)
        Scheduler.try_schedule()
        time.sleep(5)

def SchedulerService():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_scherduler_pb2_grpc.add_SchedulerServiceServicer_to_server(server_scherduler_pb2_grpc.SchedulerServiceServicer(Scheduler), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

def schedule(jobid):

    min_name, min_GPU_ID = Scheduler.get_min_load()
    if min_name == None:
        return False
    (ip, port) = next(iter(Scheduler.worker_table.get(min_name)))

    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = server_scherduler_pb2_grpc.WorkerServiceStub(channel)

        ReplyResult = stub.AccpetJob(server_scherduler_pb2.JobInformation(
            GPU_ID = min_GPU_ID, JobID= jobid
            ))
        
    if ReplyResult.response == 'successful':
        print(jobid, "schedule successful")
        return True
    
    if ReplyResult.response == 'Lose':
        print(jobid,"schedule lose" )
        return False

def start_cluster():
    jobs = generate_jobs()
    time.sleep(10)
    for i in jobs:
        if not schedule(i.jobid):
            job_queue.append(i.jobid)
    
        time.sleep(50)
        for j in list(job_queue):
            print(j)

    

