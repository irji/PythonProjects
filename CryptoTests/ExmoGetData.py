import json
import requests
import time
from requests import Response

# r: Response = requests.get('https://api.exmo.com/v1/currency/')

# obj = json.loads(r.text)
# print(json.dumps(obj, sort_keys=True, indent=4, separators=(',',': ')))

i1="ETH_USD"
i2="ETH_LTC"
i3="LTC_USD"

invest=100

open("log.txt", "w")

min=1000
max=-1000

while True:

    r1 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i1)
    r2 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i2)
    r3 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i3)

    obj1 = json.loads(r1.text)
    obj2 = json.loads(r2.text)
    obj3 = json.loads(r3.text)

    #print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    i1Vol=invest/float(obj1[i1]['ask_top'])
    i2Vol=i1Vol*float(obj2[i2]['ask_top'])
#    i3Vol=i2Vol*float(obj3[i3]['ask_top'])
    i3Vol=i2Vol*float(obj3[i3]['bid_top'])

    percent=((i3Vol - invest)/invest)*100

    if percent > max:
        max=percent

    if percent < min:
        min=percent

    text = str.format("{10}: [{0};{1}]; {2}; {11}: [{3};{4}]; {5}; {12}: [{6};{7}]; {8}; {9}% [{13}%-{14}%]",
                      obj1[i1]['ask_top'], obj1[i1]['bid_top'], str(i1Vol), obj2[i2]['ask_top'], obj2[i2]['bid_top'],
                      str(i2Vol), obj3[i3]['ask_top'], obj3[i3]['bid_top'], format(i3Vol, ".3f"), format(percent, ".3f"),
                      i1, i2, i3, format(min, ".3f"), format(max, ".3f"))

    print(text)

    #print(
    #        "ETH_USD: [", obj1[i1]['ask_top'], ";", obj1[i1]['bid_top'], "] ", i1Vol,
    #        "; ETH_LTC: [", obj2[i2]['ask_top'], ";", obj2[i2]['bid_top'], "] ", i2Vol,
    #        "; LTC_USD: [", obj3[i3]['ask_top'], ";", obj3[i3]['bid_top'], "] ", i3Vol,
    #        "; ", percent*100, "%"
    #)

    with open("log.txt", "a") as fl:
        fl.write(text + "\n")

    time.sleep(1)

#fl.close()
