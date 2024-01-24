import subprocess
import time


def OpenMPS(UUID):
    cmd  = f'export CUDA_VISIBLE_DEVICES={UUID} && export  CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && sudo -E nvidia-cuda-mps-control -d && echo $CUDA_MPS_PIPE_DIRECTORY'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    read = str(p.stdout.read())

    cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && export  CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && python warmup.py'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()



def CloseMPS(UUID):
    cmd  = f'export CUDA_VISIBLE_DEVICES={UUID} && export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && echo quit | sudo -E nvidia-cuda-mps-control '
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    read = str(p.stdout.read())


def SetPercentage(UUID, Percentage):
    cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && echo  get_server_list | sudo -E nvidia-cuda-mps-control'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    read = str(p.stdout.read().decode())
    server_ID = int(read)

    cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && sudo echo set_active_thread_percentage {server_ID} {Percentage} |sudo -E nvidia-cuda-mps-control'

    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()


def GetPercentage(UUID):
    cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && echo  get_server_list | sudo -E nvidia-cuda-mps-control'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    read = str(p.stdout.read().decode())
    server_ID = int(read)

    cmd = f'export CUDA_VISIBLE_DEVICES={UUID} && export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps-{UUID} && export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log-{UUID} && sudo echo get_active_thread_percentage {server_ID}  |sudo -E nvidia-cuda-mps-control'
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    p.wait()
    read = str(p.stdout.read().decode().strip())
    SM_percentage = float(read)
    return SM_percentage



