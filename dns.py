import re
import subprocess
import csv
import os
import glob
import xlsxwriter

providers = [
    ('1.1.1.1', 'cloudflare'), 
    ('4.2.2.1', 'level3'),
    ('8.8.8.8', 'google'),
    ('9.9.9.9', 'quad9'),
    ('80.80.80.80', 'freenom'),
    ('208.67.222.123', 'opendns'),
    ('199.85.126.20', 'norton'),
    ('185.228.168.168', 'cleanbrowsing'), 
    ('77.88.8.7', 'yandex'),
    ('176.103.130.132', 'adguard'),
    ('156.154.70.3', 'neustar'),
    ('8.26.56.26', 'comodo'),
    ('82.209.240.241', 'beltelecom'),
    #('213.184.224.254 ', 'atlant'),
    ('213.184.238.6', 'cosmos'),
    #('172.17.128.1', 'MTC'),
    ('77.74.32.42', 'velcom')
]

domainsForTest = [
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

def getDnsFromResolfCOnf():
    resolfObj = open('/etc/resolv.conf', 'r')
    resolfConf = resolfObj.readlines()

    for line in resolfConf:
        if 'nameserver ' in line:
            ip = ''.join(re.findall(r'[0-9]+(?:\.[0-9]+){3}', line))
    resolfObj.close()

    return ip

def setDnsToProvidersList(ip, name):
    providers.insert(0, (ip, name))

def checkDnsServer(provider):
    print(provider[1], end='\t\t')
    fullQueryTime = 0
    queryTimesList = [provider[1]]

    def getQueryTime(domain):
        getQueryTimeCommand = 'dig +tries=1 +time=2 +stats @' + provider[0] + ' ' + domain + ' |grep "Query time:" | cut -d : -f 2- | cut -d " " -f 2'
        queryTime = ''.join(re.findall(r'\d+', str(subprocess.check_output(getQueryTimeCommand, shell=True))))

        if not queryTime:
            queryTime = '1000'
        if queryTime == '0':
            queryTime = '1'

        return queryTime
    
    def calculateFullQueryTime(queryTime):
        return fullQueryTime + int(queryTime)

    def calculateAverageQueryTime(fullQueryTime):
        return round(fullQueryTime / len(domainsForTest))

    for domain in domainsForTest:
        queryTime = getQueryTime(domain)
        queryTimesList.append(queryTime)
        print(queryTime + ' ms', end='\t')

        fullQueryTime = calculateFullQueryTime(queryTime)

    matrixQueryTimes.append(queryTimesList)
    averageQueryTime = calculateAverageQueryTime(fullQueryTime)
    print(str(averageQueryTime) + ' ms', end='\n')

def convertMatrixOfQueryTimeToCSV():
    queryTimesStats = open('queryTimesStats.csv','w')
    queryTimesStats.seek(0)
    queryTimesStats.truncate()
    wr = csv.writer(queryTimesStats, quotechar=None)
    wr.writerows(matrixQueryTimes)
    wr.writerows([domainsForTest])
    queryTimesStats.close()

def exportCSVToExcelAndCreateChart():
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        workbook = xlsxwriter.Workbook(csvfile[:-4] + '.xlsx', {'strings_to_numbers': True})
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
                
    chart = workbook.add_chart({'type': 'line'})

    i = 0
    while i < len(providers):
        k = i + 1
        chart.add_series({
            'name':       ['Sheet1', i, 0],
            'categories': ['Sheet1', 16, 0, 16, 8],
            'values':     ['Sheet1', k, 1, k, 9]
        })  
        i = i + 1

    chart.set_title ({'name': 'DNS performance compared'})
    chart.set_x_axis({'name': 'Domains'})
    chart.set_y_axis({
        'name': 'Query time (ms)',
        'min': 0,
        'max': 200
    })
    worksheet.insert_chart('K1', chart, {'x_scale': 2, 'y_scale': 3})
    workbook.close()

dns = getDnsFromResolfCOnf()
setDnsToProvidersList(dns, dns)

print('\t\t\t', end='')
for domain in domainsForTest:
    print(domain, end='\t')
print('Average')

matrixQueryTimes = []

for provider in providers:
    checkDnsServer(provider)

convertMatrixOfQueryTimeToCSV()
exportCSVToExcelAndCreateChart()