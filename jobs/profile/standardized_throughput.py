import glob
import csv
class job:
    def __init__(self, model_name, config, batch_Size, average_time, tail):
        self.model_name = model_name
        self.config = config
        self.batch_Size = batch_Size
        self.average_time = average_time
        self.tail = tail
    def __str__(self):
        return f"Model Name: {self.model_name} Config: {self.config} Batch Size: {self.batch_Size} Average Time: {self.average_time} Tail: {self.tail}"


def get_job_list():
    job_list = []
    dir = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/offline_result/'
    file_list = glob.glob(dir+"*")

    for file_name in file_list:
        with open(file_name, 'r') as f:
            file_name = file_name.replace("/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/offline_result/", "")

            model_name = file_name
  
            for line in f:
                results = line.split(" ")
                tep_job = job(model_name= model_name, config=results[0], batch_Size=None, average_time=results[1].strip(), tail=None)
                job_list.append(tep_job)
    
        f.close()
    
    dir = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/online_result/'
    file_list = glob.glob(dir+"*")
    for file_name in file_list:
        with open(file_name, 'r') as f:
            file_name = file_name.replace("/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/online_result/", "")

            model_name = file_name
            for line in f:
                results = line.split(" ")
                tep_job = job(model_name= model_name, config=results[0], batch_Size=int(results[2].strip()), average_time=results[3].strip(), tail=None)
                job_list.append(tep_job)
    
        f.close()

    return job_list


def standardlized_single():
    dir = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/result/'

    job_list = get_job_list()
    # batch_size = []
    model_name = []
    config = []

    for i in job_list:
        if i.batch_Size:
            continue
        if i.model_name not in model_name:
            model_name.append(i.model_name)

        # if i.batch_Size not in batch_size:
        #     batch_size.append(i.batch_Size)
        
        if i.config not in config:
            config.append(i.config)

    base_dic = {}
    for i in model_name:
        base_dic[i] = {}

    for i in job_list:
        if i.batch_Size:
            continue
        if i.config == 'baseline':
            base_dic[i.model_name] = i.average_time


    throught_dic = {}
    for i in model_name:
        throught_dic[i] = {}
        for j in config:
            throught_dic[i][j] = {}

    for i in job_list:
        if i.batch_Size:
            continue
        if  i.average_time != 'error':
            throught = float(base_dic[i.model_name])/ float(i.average_time)
            if throught >= 1:
                throught = 1
            throught_dic[i.model_name][i.config] = throught
        else:
            throught_dic[i.model_name][i.config] = "error"
    


    with open(dir+"single_standardlized", "a+") as file:
        for i in model_name:
                for z in config:
                    input = i  + " " + z + " " +  str(throught_dic[i][z]) + "\n"
                    file.write(input)
    file.close()


def standardlized_double():
    dir = '/home/zbw/MIG/MIG_Schedule/jobs/profile/'
    base_dic =  standardlized_single()

    run_list = []
    with open('/home/zbw/MIG/MIG_Schedule/jobs/profile/result/2.txt', 'r') as f:
        for line in f:
            line = line.strip()
            line_list = line.split(" ")
            run_list.append(line_list)

    f.close()


    with open(dir+"double_base_standardlized", "a+") as file:
        # input = i + " " + str(j) + " " + z + " " +  str(throught_dic[i][j][z]) + "\n"
        
        for i in run_list:
            model1 = i[0]
            model2 = i[3]
            batch1 = i[1]
            batch2 = i[4]
            throught1 =  base_dic[model1][int(batch1)] / float(i[2])
            throught2 =  base_dic[model2][int(batch2)] / float(i[5])
            input = model1 + " " + str(batch1) + " " + str(throught1) + " " + model2 + " " +str(batch2) + " " + str(throught2) + "\n" 
            file.write(input)
    file.close()

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_throught_single_list():
    path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/result/single_standardlized'
    job_list = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            lines = line.split(" ")
            job_list.append(lines)
    f.close()
    return job_list


def get_throughput_double_list():
    throught_list = {}
    file_path = '/data/zbw/MIG/MIG/MIG_Schedule/jobs/profile/result/2'
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


if __name__ == "__main__":
    pass
    # standardlized_single()
    # get_job_list()
    # standardlized_single()