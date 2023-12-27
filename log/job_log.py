from datetime import datetime
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