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

    percent=(i3Vol - invest)/invest

    print(
            "ETH_USD: [", obj1[i1]['ask_top'], ";", obj1[i1]['bid_top'], "] ", i1Vol,
            "; ETH_LTC: [", obj2[i2]['ask_top'], ";", obj2[i2]['bid_top'], "] ", i2Vol,
            "; LTC_USD: [", obj3[i3]['ask_top'], ";", obj3[i3]['bid_top'], "] ", i3Vol,
            "; ", percent*100, "%"
    )

    time.sleep(2)
