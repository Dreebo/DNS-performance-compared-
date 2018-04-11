import re
import subprocess

def get_dig_command(dns_addres, domain):
    return 'dig +tries=1 +time=2 +stats @{0} {1}'.format(dns_addres, domain)

def get_shell_output(command):
    output = ''

    try:
        output = str(subprocess.check_output(command, shell=True))
    
    except Exception:
        output = 'Query time: 1000'

    return output

def get_time_from_dig_output(dig_output):
    matches = re.search(r'Query time: (\d+)', dig_output)

    return matches.group(1)

def get_query_time(dns_addres, domain):
    dig_output = get_shell_output(get_dig_command(dns_addres, domain))

    return int(get_time_from_dig_output(dig_output))