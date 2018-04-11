import os
import matplotlib.pyplot as plt
import numpy as np

import dns_check as dnsc
from print_utils import *

DNS_SERVERS = {
    'cloudflare' : '1.1.1.1',
    'level3': '4.2.2.1',
    'google': '8.8.8.8',
    'quad9': '9.9.9.9',
    'freenom': '80.80.80.80',
    'opendns': '208.67.222.123',
    'norton': '199.85.126.20',
    'cleanbrowsing' : '185.228.168.168',
    'yandex': '77.88.8.7',
    'adguard': '176.103.130.132',
    'neustar': '156.154.70.3',
    'comodo': '8.26.56.26',
    'beltelecom': '82.209.240.241',
    'cosmos': '213.184.238.6',
    'velcom': '77.74.32.42'
}

DOMAINS = [
    'google.com',
    'amazon.com',
    'facebook.com',
    'youtube.com',
    'reddit.com',
    'wikipedia.org',
    'twitter.com',
    'gmail.com',
    'whatsapp.com'
]

if __name__ == "__main__":
    domains_times_result = {}

    for dns, addres in DNS_SERVERS.items():
        print()        
        print_with_background('Checking {0} dns:'.format(dns))
        print()

        domains_times_result[dns] = dnsc.get_query_time(addres, DOMAINS)

    os.system('clear')

    for dns, results in domains_times_result.items():
        print_title(dns)
        print()
        print_with_background('{0: <20}{1: <15}{2: <60}'.format('Domain', 'Average (ms)', 'Results (ms)'))
        
        average_results = []

        for index, (domain, domain_results) in enumerate(results.items()):
            average_results.append(domain_results[0])

            results = '{0}'.format(', '.join(str(x) for x in domain_results[1]))

            line = '{0: <20}{1: <15}{2: <60}'.format(domain, domain_results[0], results)

            if index % 2 == 0:
                print_even_table_line(line)
            else:
                print_odd_table_line(line)
        print('\n\n')

        plt.plot(average_results, label=dns)

plt.xticks(np.arange(len(DOMAINS)), DOMAINS)
plt.xlabel('Domains')
plt.ylabel('Query time (ms)')
plt.legend()
plt.show()