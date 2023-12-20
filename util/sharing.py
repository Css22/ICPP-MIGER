import glob
import json
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
        self.gi_id = -1 
        self.model_name = model_name
        self.batch_Size = batch_Size
        self.qos = qos
        self.jobid = jobid

    def __str__(self):
        return f"online Model Name: {self.model_name}  Batch Size: {self.batch_Size} QOS : {self.qos}"

class offline_job: 
    def __init__(self, model_name, batch_Size, epoch, jobid=0):
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