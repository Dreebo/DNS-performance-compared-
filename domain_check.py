import dig
from numpy import average
from tqdm import tqdm

EXECUTION_COUNT = 10

def get_query_time(dns_addres, domain):
    execution_times = []

    for i in tqdm(range(0, EXECUTION_COUNT)):
        execution_times.append(dig.get_query_time(dns_addres, domain))

    average_time = average(execution_times)

    return average_time, execution_times