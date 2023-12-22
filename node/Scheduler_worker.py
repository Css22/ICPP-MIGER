import grpc
import grpc_tool.server_scherduler_pb2_grpc as server_scherduler_pb2_grpc
import grpc_tool.server_scherduler_pb2 as  server_scherduler_pb2 
from concurrent import futures
import threading
import configs.configs as configs

class SchedulerObject:
    def __init__(self):
        self.worker_table = {}
        self.load = {}
        self.load_list = {}
        self.lock = threading.Lock()

    def add_worker(self, request):
        with self.lock:
            self.worker_table[request.name] = {(request.ip, request.port)}
            self.load[request.name] = {}
            self.load_list[request.name] = {}

    def update_load(self, request):
        with self.lock:
            self.load[request.name][request.GPU_ID] = request.load
        print(self.load)


Scheduler = SchedulerObject()

def SchedulerService():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_scherduler_pb2_grpc.add_SchedulerServiceServicer_to_server(server_scherduler_pb2_grpc.SchedulerServiceServicer(Scheduler), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


