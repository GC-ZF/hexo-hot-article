'''
转自：https://github.com/Zfour/python_github_calendar_api
'''
import requests
import re

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
def get_calendar(name):
    gitpage = requests.get("https://github.com/" + name)
    data = gitpage.text
    datadatereg = re.compile(r'data-date="(.*?)" data-level')
    datacountreg = re.compile(r'<span class="sr-only">(.*?) contribution')
    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    datacount = list(map(int, [0 if i == "No" else i for i in datacount]))

    # 将datadate和datacount按照字典序排序
    sorted_data = sorted(zip(datadate, datacount))
    datadate, datacount = zip(*sorted_data)
    
    contributions = sum(datacount)
    datalist = []
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata
