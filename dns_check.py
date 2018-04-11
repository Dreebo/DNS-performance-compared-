import domain_check as domainc
from tqdm import tqdm

from print_utils import print_title

def get_query_time(dns_addres, domains):
    domain_times = {}

    for domain in domains:
        print_title('Calculate results for {0}: '.format(domain))
        domain_times[domain] = domainc.get_query_time(dns_addres, domain)

    return domain_times

    