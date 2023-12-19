import glob
class job:
    def __init__(self, model_name, config, batch_Size, average_time, tail):
        self.model_name = model_name
        self.config = config
        self.batch_Size = batch_Size
        self.average_time = average_time
        self.tail = tail
    def __str__(self):
        return f"Model Name: {self.model_name} Config: {self.config} Batch Size: {self.batch_Size} Average Time: {self.average_time} Tail: {self.tail}"


class online_job:
    def __init__(self, model_name, batch_Size, qos):
        self.gi_id = -1 
        self.model_name = model_name
        self.batch_Size = batch_Size
        self.qos = qos

    def __str__(self):
        return f"online Model Name: {self.model_name}  Batch Size: {self.batch_Size} QOS : {self.qos}"

class offline_job: 
    def __init__(self, model_name, batch_Size, epoch):
        self.model_name = model_name
        self.batch_Size = batch_Size
        self.epoch = epoch
        self.submit_time = 0
        self.start_time = -1
        self.progress = 0
        self.end_time = None
        self.speed = 0



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
