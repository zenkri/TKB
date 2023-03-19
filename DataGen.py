import pickle

import pandas as pd
import datetime
import random
import time
import numpy as np
import pickle as pkl


def gaussian(mean, std):
    return (1 / (std* np.sqrt(2*np.pi))) * np.exp(-0.5*(mean / std)**2)


def random_time():
    return datetime.time(random.randint(8, 17), random.randint(0, 59), random.randint(0, 59))

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)


cusomer_ids = ['cus_' + str(i) for i in range(1000)]
start_date = datetime.date(2023, 3, 11)
end_date = datetime.date(2023, 3, 18)
delta = end_date - start_date
dates = [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]

avg_autom_wait = 60
std_autom_wait = 40

avg_autom_dur = 40
std_autom_dur = 40

avg_info_wait = 60
std_info_wait = 100

avg_info_dur = 100
std_info_dur = 180

avg_schalt_dur = 180
std_schalt_dur = 180

avg_schalt_wait = 120
std_schalt_wait = 120


location = ['Automat', 'Info', 'Schalter']

dataset = {'customer': [], 'date': [], 'time': [], 'location': [], 'duration': [], 'wait_time': [], 'event': [], 'time_h': [], 'day': []}

for ii in range(5000):
    dataset['customer'].append(random.choice(cusomer_ids))
    dataset['date'].append(random_date('3/11/2023', '3/18/2023', random.random()))
    dataset['time'].append(random_time())
    dataset['time_h'].append(dataset['time'][-1].hour + dataset['time'][-1].minute / 60)
    dataset['location'].append(np.random.choice(location, p=[0.65, 0.15, 0.2]))
    if dataset['location'][-1] == 'Automat':
        dataset['day'].append(np.random.choice(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'], p=[0.14, 0.14, 0.14, 0.14, 0.16, 0.14, 0.14]))
    else:
        dataset['day'].append(np.random.choice(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'], p=[0.2, 0.2, 0.2, 0.2, 0.2, 0, 0]))

    if dataset['location'][-1] == 'Automat':
        dataset['duration'].append(max(15, np.random.normal(avg_autom_dur, std_autom_dur)) * gaussian(dataset['time'][-1].hour - 15, 2))
    elif dataset['location'][-1] == 'Info':
        dataset['duration'].append(max(10, np.random.normal(avg_info_dur, std_info_dur)) * gaussian(dataset['time'][-1].hour - 15, 8))
    elif dataset['location'][-1] == 'Schalter':
        dataset['duration'].append(max(25, np.random.normal(avg_schalt_dur, std_schalt_dur)) * gaussian(dataset['time'][-1].hour - 15, 4))


    if dataset['location'][-1] == 'Automat':
        dataset['wait_time'].append(np.random.choice([0, max(5, np.random.normal(avg_autom_wait, std_autom_wait))], p=[0.4, 0.6]) * gaussian(dataset['time'][-1].hour - 15, 2))
    elif dataset['location'][-1] == 'Info':
        dataset['wait_time'].append(np.random.choice([0, max(5, np.random.normal(avg_info_wait, std_info_wait))], p=[0.1, 0.9]) * gaussian(dataset['time'][-1].hour - 15, 8))
    elif dataset['location'][-1] == 'Schalter':
        dataset['wait_time'].append(np.random.choice([0, max(5, np.random.normal(avg_schalt_wait, std_schalt_wait))], p=[0.2, 0.8]) * gaussian(dataset['time'][-1].hour - 15, 4))

    dataset['event'].append(1)

data_frame = pd.DataFrame.from_dict(dataset)

with open('./dataset.pkl', 'wb') as f:
    pickle.dump(data_frame, f)
    f.close()






