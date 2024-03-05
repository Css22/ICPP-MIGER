from datetime import datetime
from util.sharing import *
def record_job_state(jobid, state, path = './log/job_log'):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, 'a') as file:
        log = formatted_date + ' ' +  str(jobid) + ' ' + str(state)+'\n'
        file.write(log)

def record_node_load(load, path='./log/load_log'):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(path, 'a') as file:
        log = formatted_date + ' ' + str(load)+ '\n'
        file.write(log)


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
        flag = False
        pause_time = 0
        flag_time = None
        time_table[i.jobid]['queue_time'] = None
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
                        if flag != 0:
                            flag = False
                            pause_time = (timestamp - flag_time).total_seconds() + pause_time


                    if action == 'pause':
                        flag = True
                        flag_time = timestamp

                    if action == 'queue':
                        time_table[i.jobid]['queue_time'] = timestamp


        file.close()  
        time_table[i.jobid]['pause'] = pause_time
    


    JCT = 0
    makespan = 0
    start_time = '2024-04-04 00:00:00'
    end_time = '2023-09-01 00:20:10'
    queue_time = 0



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
    


    for i in time_table.keys():
        if time_table[i]['queue_time']:
            start_time = time_table[i]['start']
            queue_time = queue_time + (start_time - time_table[i]['queue_time']).total_seconds()

    queue_time = queue_time/len(offline_job_list)
    

    pause_time = 0
    for i in time_table.keys():
        pause_time = pause_time +  time_table[i]['pause'] 
        print(time_table[i]['pause'] )
    
    pause_time = pause_time/len(offline_job_list)
    print("MakeSpan: " + str(makespan.total_seconds()))
    print("JCT: " + str(JCT))
    print("queue_time: "  + str(queue_time))
    print("pause_time: " + str(pause_time))