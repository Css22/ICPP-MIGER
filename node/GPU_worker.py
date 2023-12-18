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
import socket
class GPU_monitor:
    def __init__(self):
        self.running = True

    def start_GPU_monitor(self, gpu_id, gi_id):
        while self.running:
            cmd = f'dcgmi dmon -e 1002 -d 1000 -i {gpu_id}/{gi_id}'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True)

            while self.running:
                output = process.stdout.readline()
                output = output.strip()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    if len(output.split()) != 3:
                        continue
                    else:
                        load_submission(gpu_id=int(gpu_id), GI_ID=int(gi_id), load= float(output.split()[2]) * 100)
        load_submission(gpu_id=int(gpu_id), GI_ID=int(gi_id), load= -1)

    def stop(self):
        self.running = False

ip='10.16.56.14'
port=50052
node = socket.gethostname()

num_GPU = 1
UUID_table = {

}

static_partition = {

}

monitor_table = {

}

for i in range(0, num_GPU):
    UUID_table[i] = {

    }

    static_partition[i] = []

    monitor_table[i] = {

    }

def WorkerService():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_scherduler_pb2_grpc.add_WorkerServiceServicer_to_server(server_scherduler_pb2_grpc.WorkerServiceServicer(), server)
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

def load_submission(gpu_id, GI_ID, load):
    global ip, port, node
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = server_scherduler_pb2_grpc.SchedulerServiceStub(channel)

        Load = stub.Load(server_scherduler_pb2.LoadInformation(
            name = node, GPU_ID=gpu_id , GI_ID= GI_ID, load = load
            ))