import json
import requests
import time
from requests import Response

# r: Response = requests.get('https://api.exmo.com/v1/currency/')

# obj = json.loads(r.text)
# print(json.dumps(obj, sort_keys=True, indent=4, separators=(',',': ')))

i1 = "ETH_USD"
i2 = "ETH_LTC"
i3 = "LTC_USD"

i4 = "ETH_EUR"
i5 = "ETH_LTC"
i6 = "LTC_EUR"


invest = 100

open("log.txt", "w")
open("log2.txt", "w")

min1 = min2 = 1000
max1 = max2 = -1000

while True:

    r1 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i1 + "," + i2 + "," + i3)
    r2 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i4 + "," + i5 + "," + i6)
    #r2 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i2)
    #r3 = requests.get('https://api.exmo.com/v1/order_book/?pair=' + i3)

    obj1 = json.loads(r1.text)
    obj2 = json.loads(r2.text)
    #obj3 = json.loads(r3.text)

    # print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

    i1Vol1 = invest / float(obj1[i1]['ask_top'])
    i2Vol1 = i1Vol1 * float(obj1[i2]['ask_top'])
    #    i3Vol=i2Vol*float(obj3[i3]['ask_top'])
    i3Vol1 = i2Vol1 * float(obj1[i3]['bid_top'])

    i1Vol2 = invest / float(obj2[i4]['ask_top'])
    i2Vol2 = i1Vol2 * float(obj2[i5]['ask_top'])
    #    i3Vol=i2Vol*float(obj3[i3]['ask_top'])
    i3Vol2 = i2Vol2 * float(obj2[i6]['bid_top'])


    percent1 = ((i3Vol1 - invest) / invest) * 100
    percent2 = ((i3Vol2 - invest) / invest) * 100


    if percent1 > max1:
        max1 = percent1

    if percent1 < min1:
        min1 = percent1

    if percent2 > max2:
        max2 = percent2

    if percent2 < min2:
        min2 = percent2

    text = str.format("{10}: [{0};{1}]; {2}; {11}: [{3};{4}]; {5}; {12}: [{6};{7}]; {8}; {9}% [{13}%-{14}%]",
                      obj1[i1]['ask_top'], obj1[i1]['bid_top'], format(i1Vol1, ".6f"), obj1[i2]['ask_top'],
                      obj1[i2]['bid_top'],
                      format(i2Vol1, ".6f"), obj1[i3]['ask_top'], obj1[i3]['bid_top'], format(i3Vol1, ".3f"),
                      format(percent1, ".3f"),
                      i1, i2, i3, format(min1, ".3f"), format(max1, ".3f"))

    text2 = str.format("{10}: [{0};{1}]; {2}; {11}: [{3};{4}]; {5}; {12}: [{6};{7}]; {8}; {9}% [{13}%-{14}%]",
                      obj2[i4]['ask_top'], obj2[i4]['bid_top'], format(i1Vol2, ".6f"), obj2[i5]['ask_top'],
                      obj2[i5]['bid_top'],
                      format(i2Vol2, ".6f"), obj2[i6]['ask_top'], obj2[i6]['bid_top'], format(i3Vol2, ".3f"),
                      format(percent2, ".3f"),
                      i4, i5, i6, format(min2, ".3f"), format(max2, ".3f"))
    print(text)
    print(text2)

    # print(
    #        "ETH_USD: [", obj1[i1]['ask_top'], ";", obj1[i1]['bid_top'], "] ", i1Vol,
    #        "; ETH_LTC: [", obj2[i2]['ask_top'], ";", obj2[i2]['bid_top'], "] ", i2Vol,
    #        "; LTC_USD: [", obj3[i3]['ask_top'], ";", obj3[i3]['bid_top'], "] ", i3Vol,
    #        "; ", percent*100, "%"
    # )

    with open("log.txt", "a") as fl:
        fl.write(text + "\n")

    with open("log2.txt", "a") as fl2:
        fl2.write(text2 + "\n")

    time.sleep(1)

# fl.close()
