import subprocess
import time
import re
import socket
node = socket.gethostname()
Configurations_map = {1: '1g.10gb', 2 : '2g.20gb' , 3: '3g.40gb', 4: '4g.40gb', 7: '7g.80gb'}
map_table = {0:0, 2:1, 1:2, 5:3 , 6:4, 3:5, 11:7, 12:8, 13:9, 14:10, 7:11, 8:12, 9:13}
reversed_map_table = {0:0, 1:2, 2:1, 3:5, 4:6, 5:3, 7:11, 8:12, 9:13, 10:14, 11:7, 12:8, 13:9}
def init_mig():
    for gpu in range(2):
        cmd = f'./enable_mig.sh {gpu}'
        p = subprocess.Popen([cmd], shell=True)
        p.wait()
   
def disable_mps():
    cmd = f'sudo pkill -9 nvidia-cuda-mps'
    p = subprocess.Popen([cmd], shell=True)
    p.wait()

def disable_mig():
    for gpu in range(2):
        cmd = f'sudo nvidia-smi -i {gpu} -mig 0'
        p = subprocess.Popen([cmd], shell=True)
        p.wait()

def reset_mig(gpu):
    cmd = f'sudo nvidia-smi mig -i {gpu} -dci'
    # Note: need to make sure the reset is successful
    success = False
    while not success:
        p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
        p.wait()
        read = str(p.stdout.read())
        if 'Unable to destroy' not in read:
            success = True
        else:
            print('Trying again...')
            time.sleep(0.5)
    cmd = f'sudo nvidia-smi mig -i {gpu} -dgi'
    p = subprocess.Popen([cmd], shell=True)
    p.wait()

def create_ins(gpu, ins):
    id_map = {'1c-1g-10gb': 19, '1c-2g-20gb': 14, '1c-3g-40gb': 9, '1c-4g-40gb': 5, '1c-7g-80gb': 0}
    ins_code = id_map[ins]
    cmd = f'sudo nvidia-smi mig -i {gpu} -cgi {ins_code} -C'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    read = str(p.stdout.read())
    ID = re.findall(r'\d+', read)[0]
    print(f"create instance with ID {ID} with GPU ID {gpu}")
    # need to retrieve GPU instance ID from output
    # cmd = f'sudo nvidia-smi mig -i {gpu} -gi {ID} -cci'
    # p = subprocess.Popen([cmd], shell=True)
    # p.wait()
    time.sleep(2)
    return ID

def destroy_ins(gpu, ID):
    if node == 'hpclab04' and int(gpu) == 2:
        ID = reversed_map_table[int(ID)]
    cmd = f'sudo nvidia-smi mig -dci -i {gpu} -gi {ID} -ci 0 && sudo nvidia-smi mig -dgi -i {gpu} -gi {ID}'
    p = subprocess.Popen([cmd], shell=True)
    p.wait()

def create_ins_with_ID(gpu, ins, req_ID):
    if node == 'hpclab04' and int(gpu) == 2:
        req_ID = reversed_map_table[int(req_ID)]
    tem_ID_list = []
    while True:
        ID = create_ins(gpu, ins)
        if int(ID) == int(req_ID):
            for i in tem_ID_list:
                destroy_ins(gpu, i)
            print(f"create instance with ID {req_ID}")
            if node == 'lab04' and int(gpu) == 2:
                ID = map_table[int(ID)]
            return ID
        else:
            tem_ID_list.append(ID)
  
            
def do_partition(gpu, partition): # partition is a list of slice # code is partition code, e.g. '0', '1',...
    id_map = {1: 19, 2: 14, 3: 9, 4: 5, 7: 0}
    ins_code = [str(id_map[k]) for k in partition]
    code_str = ','.join(ins_code)
    cmd = f'sudo nvidia-smi mig -i {gpu} -cgi {code_str}'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    cmd = f'sudo nvidia-smi mig -i {gpu} -cci'
    p = subprocess.Popen([cmd], shell=True)
    p.wait()


def get_uuid(gpu_id):
    process = subprocess.Popen(['nvidia-smi', '-L'], stdout=subprocess.PIPE, text=True)
    flag = False
    end_flag = False
    UUID_list = []
    while True:
        line = process.stdout.readline()
        if not line:
            break

        gpu_pattern = re.compile(rf'GPU {gpu_id}: .* \(UUID: GPU-(.*?)\)')
        gpu_match = gpu_pattern.search(line)
        gpu_pattern_next = re.compile(rf'GPU {gpu_id + 1}: .* \(UUID: GPU-(.*?)\)')
        gpu_match_next = gpu_pattern_next.search(line)
        if gpu_match_next:
            end_flag = True
            continue
        if gpu_match:
            flag = not flag
            continue
        if flag and not end_flag:
            match = re.search(r'MIG-[\da-fA-F\-]+', line.strip())
            uuid = match.group()
            UUID_list.append(uuid)
    return UUID_list

